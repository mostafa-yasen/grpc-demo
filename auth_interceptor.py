import grpc
import jwt
import os
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

SECRET_KEY = os.getenv("SECRET_KEY")


def validate_token(token):
    try:
        # Decode the token using your secret key
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        logging.error(f"Token expired {token}")
        # Raise RpcError with status code 'UNAUTHENTICATED' and proper message
        raise grpc.RpcError("Expired token", grpc.StatusCode.UNAUTHENTICATED)
    except jwt.InvalidTokenError:
        logging.error(f"Invalid token {token}")
        # Raise RpcError with status code 'UNAUTHENTICATED' and proper message
        raise grpc.RpcError("Invalid token", grpc.StatusCode.UNAUTHENTICATED)
    except Exception as e:
        logger.error(f"Unknown Issue: {e}")

        # Raise RpcError with status code 'UNKNOWN' and proper message
        raise grpc.RpcError(
            "Unknown issue while decoding the token", grpc.StatusCode.UNKNOWN
        )


class AuthInterceptor(grpc.ServerInterceptor):
    def _rpc_terminator(self, code, details):
        def terminate(ignored_request, context):
            context.abort(code, details)

        return terminate

    def intercept_service(self, continuation, handler_call_details):
        # Extract metadata
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get("authorization")

        if not token:
            return self._rpc_terminator(
                grpc.StatusCode.UNAUTHENTICATED,
                "Authorization token is missing",
            )

        # Validate the token
        try:
            payload = validate_token(token)
        except grpc.RpcError as e:
            return grpc.unary_unary_rpc_method_handler(
                self._rpc_terminator(e.code(), e.details())
            )

        # Continue the RPC
        return continuation(handler_call_details)
