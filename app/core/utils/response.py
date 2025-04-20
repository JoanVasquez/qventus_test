# 🎯 Creates a standardized success response format
def success_response(data=None, message="Success", code=200):
    return {
        "success": True,         # ✅ Indicates successful operation
        "message": message,      # 💬 Custom success message
        "data": data,            # 📦 Optional data payload
        "code": code             # 🔢 HTTP status code
    }


# ⚠️ Creates a standardized error response format
def error_response(
    message="An error occurred", code="error", details=None, status_code=400
):
    return {
        "success": False,        # ❌ Indicates failure
        "error": {
            "code": code,        # 🆔 Error code identifier
            "message": message,  # 💬 Human-readable error message
            "details": details   # 🧾 Optional validation or debug info
        },
        "code": status_code      # 🔢 HTTP status code
    }
