# TKB NTMK

Phần mềm xếp thời khóa biểu nội bộ cho Trường TH-THCS-THPT Nguyễn Thị Minh Khai.

## Mục tiêu

- Xếp **toàn bộ giáo viên và lớp của trường**.
- Thu lịch rảnh giáo viên bằng **Google Form → Google Sheets**.
- Dùng **Google OR-Tools CP-SAT** để xử lý ràng buộc cứng và tối ưu chất lượng lịch.
- Ưu tiên giảm **tiết lủng**, giảm ngày phải dạy cả sáng + chiều, và tạo **ngày nghỉ** cho giáo viên khi có thể.
- Chạy nội bộ trên máy Windows, không cần VPS.

## Dữ liệu đã nạp sẵn

Bản V0.2 đã dựng dữ liệu từ PCCM và TKB mẫu được cung cấp:

- 30 giáo viên
- 14 lớp (10A1–10A4, 11A1–11A3, 12A1–12A7)
- 182 phân công lớp/môn
- Các tiết HĐTN chung được khóa theo mẫu hiện hành

### Ràng buộc đặc thù đang bật

- **Võ:** chỉ buổi chiều, 2 tiết liên tiếp.
- **STEM:** chỉ buổi chiều; cấu hình hiện tại là đồng giảng `Tin-Minh + T-Chân`.
- **GVCN:** ưu tiên rất cao có tiết 1 với lớp chủ nhiệm.
- Không trùng giáo viên, không trùng lớp.
- Tuân thủ lịch rảnh giáo viên sau khi đồng bộ Google Form.

> Lưu ý: cấu hình STEM có thể đổi sau nếu thực tế là hai giáo viên chia lớp/luân phiên thay vì đồng giảng.

## Cài đặt Windows

Khuyến nghị dùng môi trường riêng để không ảnh hưởng TensorFlow/MediaPipe trên máy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Chạy:

```powershell
.\.venv\Scripts\python.exe app.py
```

Hoặc chạy `setup_windows.bat` một lần, sau đó `run_windows.bat`.

Phần mềm mở ở:

```text
http://localhost:8080
```

Đây là địa chỉ **trên chính máy đang chạy**, không phải website công khai.

## Quy trình sử dụng

1. Mở **Đăng ký GV**.
2. Đồng bộ Google Sheet phản hồi từ Google Form hoặc nhập CSV.
3. Vào **Ràng buộc** để chỉnh ưu tiên từng giáo viên.
4. Mở **Xếp TKB** → `XẾP TOÀN TRƯỜNG`.
5. Xem theo giáo viên/lớp.
6. Kiểm tra trang **Chất lượng**.
7. Xuất Excel/Word.

## Định dạng CSV Google Form

Phần mềm hỗ trợ dạng rộng:

```text
ma_gv,ho_ten,2-S-1,2-S-2,...,7-C-3
Tin-Minh,Nguyễn Văn Minh,1,1,...,0
```

`1` = có thể dạy, `0` = không thể dạy.

Trong trang **Đăng ký GV** có nút tải mẫu CSV sẵn 30 giáo viên.

## Cập nhật source trên máy trường

Sau khi clone repository một lần:

```powershell
git pull
.\.venv\Scripts\python.exe app.py
```

Không cần tải ZIP qua lại.
