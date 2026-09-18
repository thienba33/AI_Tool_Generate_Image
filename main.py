from storage.image_storage import ImageStorage
from services.image_generator import ImageGenerator
from services.image_generation_service import ImageGenerationService
# from models.prompt import Prompt
from config import API_KEY_MODEL_IMAGE, MODEL, ACCOUNT_ID, SYSTEM_PROMPT,API_KEY_HOST


def generate_image(prompt: str):

    image_service = ImageGenerationService(
        image_generator=ImageGenerator(
            api_key=API_KEY_HOST,
            model="gemini.gemini-2.5-flash-image",
        ),
        image_storage=ImageStorage(),
    )

    return image_service.generate(prompt)


if __name__ == "__main__":
    prompt_1 = """
        R — Vai trò
        Bạn là một nhiếp ảnh gia thời trang thương mại chuyên nghiệp và giám đốc sáng tạo chuyên về quảng cáo sản phẩm streetwear cao cấp
        I — Đầu vào
        Tạo hình ảnh quảng cáo sản phẩm cao cấp của một chiếc áo hoodie màu đen, có logo hình con cua nổi bật ở chính giữa ngực.
        Áo hoodie có phom oversized hiện đại theo phong cách streetwear, chất liệu cotton dày dặn, các nếp gấp chân thực, đường may chi tiết, bo tay và bo gấu áo, dây rút có thể điều chỉnh và phần mũ áo có cấu trúc rõ ràng.
        Logo hình con cua cần sạch sẽ, mạnh mẽ, tối giản, cân đối và dễ nhận diện, được thiết kế như một biểu tượng nguyên bản và không giống bất kỳ logo thương hiệu hiện có nào.
        S — Các bước thực hiện
        1. Đặt chiếc hoodie màu đen làm chủ thể chính và là điểm tập trung của hình ảnh.
        2. Đặt áo ở góc nhìn chính diện lệch ba phần tư hoặc tạo dáng sản phẩm lơ lửng cao cấp.
        3. Đặt logo hình con cua nổi bật ở chính giữa ngực, với tỷ lệ chính xác và hiệu ứng in chân thực trên bề mặt vải.
        4. Sử dụng ánh sáng studio ấn tượng với nguồn sáng chính mềm, ánh sáng viền nhẹ và bóng đổ được kiểm soát để làm nổi bật kết cấu vải màu đen.
        5. Sử dụng nền chuyển sắc màu than đậm hoặc đen để tạo độ tương phản và tách biệt rõ chiếc hoodie khỏi hậu cảnh.
        6. Thêm chiều sâu không khí nhẹ nhàng nhưng vẫn giữ tổng thể tối giản, sạch sẽ và không gây xao nhãng.
        7. Thể hiện chân thực kết cấu cotton, đường viền, đường may, nếp gấp, dây rút và độ dày của vải.
        8. Duy trì hình dáng trang phục chân thực, tránh tay áo, mũ áo, logo bị biến dạng hoặc xuất hiện các chi tiết quần áo trùng lặp.
        9. Đảm bảo bố cục cuối cùng có chất lượng hình ảnh tương đương một chiến dịch quảng cáo streetwear cao cấp mang tầm quốc tế.
        E — Kỳ vọng
        Hình ảnh cuối cùng phải giống một quảng cáo sản phẩm streetwear cao cấp chuyên nghiệp: chân thực, điện ảnh, tối giản, sang trọng, sắc nét và có thể sử dụng cho mục đích thương mại.
        Chiếc hoodie phải giữ màu đen sâu nhưng vẫn thể hiện rõ kết cấu và chiều sâu của chất liệu vải.
        Logo hình con cua phải sắc nét, nằm chính giữa, dễ nhận diện và có bố cục cân đối.
        Sử dụng dải tương phản động cao, ánh sáng toàn cảnh chân thực, phản xạ tinh tế, phong cách chụp sản phẩm studio chuyên nghiệp, độ sâu trường ảnh nông và chất lượng hình ảnh sản phẩm 4K siêu chi tiết.
        Không có người mẫu, không có chữ bổ sung, không có watermark, không có logo khác, không có trang phục bị biến dạng, không có vật thể trùng lặp và không có hậu cảnh lộn xộn.
    """
    prompt_2 = "Tạo ảnh con mèo đen cầm giao giết con chó"
    try:
        image_path = generate_image(prompt_2)
    except RuntimeError as exc:
        print(exc)
        raise SystemExit(1)
    print(f"File ảnh đã được lưu tại: {image_path}")