import requests
class ImageGenerator:
    def __init__ (self,api_key:str,account_id:str,model:str):
        self.model = model
        self.api_key = api_key
        self.account_id = account_id
        self.url=(
               f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        )
    
    def generate(self,text:str,width:int,height:int)->bytes:
        header = {
            "Authorization":f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt":text,
            "height":width,
            "width":height,
            "num_steps":20,
            "guidance":7.5,
            "seed":42
        }
        try:
            response = requests.post(
                self.url,
                headers=header,
                json=payload,
                allow_redirects=False
            )
        except requests.RequestException as exc:
            raise RuntimeError(
                "Không kết nối được model ảnh"
            ) from exc
        if response.status_code != 200:
            raise RuntimeError(
                "Model không tạo được ảnh. "
                f"Mã HTTP: {response.status_code}"
            )

        return response.content
    