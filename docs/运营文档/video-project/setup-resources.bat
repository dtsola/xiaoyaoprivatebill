@echo off
REM 小遥账单助手 - 视频项目资源准备脚本
REM 用途：将产品截图复制到 Remotion 项目的 public 目录

echo 正在准备视频项目资源...
echo.

REM 创建目标目录
echo [1/3] 创建 public 目录结构...
if not exist "public\screenshots" mkdir "public\screenshots"
if not exist "public\audio" mkdir "public\audio"

REM 复制截图文件
echo [2/3] 复制截图文件...
copy /Y "..\..\产品文档\产品截图\Logo.png" "public\screenshots\logo.png" >nul
copy /Y "..\..\产品文档\产品截图\08-上传账单.png" "public\screenshots\upload.png" >nul
copy /Y "..\..\产品文档\产品截图\02-年度总览.png" "public\screenshots\overview.png" >nul
copy /Y "..\..\产品文档\产品截图\04-分类分析.png" "public\screenshots\category.png" >nul
copy /Y "..\..\产品文档\产品截图\06-消费洞察-01.png" "public\screenshots\insight.png" >nul
copy /Y "..\..\产品文档\产品截图\宣传海报图.png" "public\screenshots\poster.png" >nul

echo.
echo [3/3] 资源复制完成！
echo.
echo 资源位置：
echo - 截图: public\screenshots\
echo - 音频: public\audio\ (请手动放置 voiceover.mp3)
echo.
echo 下一步：
echo 1. 录制配音 (参考 VOICEOVER_SCRIPT.md)
echo 2. 将配音文件放到 public\audio\voiceover.mp3
echo 3. 运行 npm install
echo 4. 运行 npm run dev 启动开发服务器
echo.
pause
