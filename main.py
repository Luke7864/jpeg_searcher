import os
import platform

#JPEG파일을 찾을 디렉토리 입력
# 테스트 디렉토리: .\File Signature Examples
path_dir = input("Input Directory to Search JPEG: ")

#상대경로로 입력할 경우, 절대경로로 변환
if path_dir[:2] == "./" or path_dir[:2] == ".\\":
    if platform.system() == "Windows":
        path_dir = os.getcwd() + "\\" + path_dir[2:]
    else:
        path_dir = os.getcwd() + "/" + path_dir[2:]

#마지막에 /혹은 \가 안 붙었을 경우, 운영체제에 맞게 /혹은 \ 추가
if path_dir[-1] != "\\" and path_dir[-1] != "/":
    if platform.system() == "Windows":
        path_dir += "\\"
    else:
        path_dir += "/"

file_list = []

#재귀 이용하여 하위 디렉토리 전부 탐색
for path, dirs, files in os.walk(path_dir):
    for file in files:
        file_list.append(os.path.join(path, file))

#JPEG 파일시그니처
jpeg_head_sign = [b"\xFF\xD8\xFF\xE0", b"\xFF\xD8\xFF\xE2", b"\xFF\xD8\xFF\xE3", b"\xFF\xD8\xFF\xE8"]
jpeg_foot_sign = b"\xFF\xD9"

jpeg_list = []

#JPEG 헤드시그니처와 푸터시그니처를 이용해 탐색
for file in file_list:
    isfile = os.path.isfile(file)
    if isfile == True:
        f = open(file, "rb")
        data = f.read()
        f.close()
        xdensity = int.from_bytes(data[15:17], byteorder='little')
        ydensity = int.from_bytes(data[17:19], byteorder='little')
        #Search JPEG Signature and check Xdensity/Ydensity is bigger than 0
        if data[:4] in jpeg_head_sign and data[-2:] == jpeg_foot_sign and xdensity > 0 and ydensity > 0:
            jpeg_list.append(file)

#JPEG 파일을 찾아낸 결과를 result.txt로 저장
f = open("./result.txt", "w", encoding="utf8")
f.write("JPEG Files were found from under {}\n\n".format(path_dir))
for i in jpeg_list:
    f.write(i)
    f.write("\n")
f.close()

#결과 출력
f = open("./result.txt", "r", encoding="utf8")
print(f.read())
f.close()