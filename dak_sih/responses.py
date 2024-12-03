from rest_framework.viewsets import ViewSet

class EnhancedResponseMixin(ViewSet):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        
        status_code = response.status_code
        
        if 200 <= response.status_code <= 299:
            data = dict(success=True, data=response.data)
            status_code = 200
            
        elif 400 <= response.status_code <= 499:
            if response.status_code == 403:
                message = "You are not authorized to perform this request" 
            elif response.status_code == 404 and isinstance(response.data, str):
                message = f"No matching {response.data} was found"
            elif not isinstance(response.data, list) and not response.data.get("detail"):
                message = "; ".join([
                    f"{field}: {', '.join(errors)}"
                    for field, errors in response.data.items()
                    if field != "non_field_errors"
                ])
            elif isinstance(response.data, list):
                message = "; ".join(response.data)
            else:
                message = str(response.data.get("detail"))
            
            data = dict(success=False, message=message)
            status_code = 200

        response.data = data
        response.status_code = status_code
        
        return response
