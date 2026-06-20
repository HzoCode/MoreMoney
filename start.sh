#!/bin/bash
# A股交易记录系统 - 一键启动（自动打开浏览器）
# 后端: FastAPI (port 8899) | 前端: Vite (port 5173)

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
URL="http://127.0.0.1:5173"

cleanup() {
  echo ""
  echo "正在关闭服务..."
  kill $BACKEND_PID 2>/dev/null
  kill $FRONTEND_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM

echo "============================="
echo "  A股交易记录系统 v2.0"
echo "============================="
echo ""

# 1. 安装依赖
if [ ! -d "$DIR/frontend/node_modules" ]; then
  echo "[1/3] 安装前端依赖 (pnpm)..."
  cd "$DIR/frontend" && pnpm install --silent
else
  echo "[1/3] 前端依赖 OK"
fi

# 2. 启动后端
echo "[2/3] 启动后端 (port 8899)..."
cd "$DIR/backend"
python3 -m uvicorn main:app --host 127.0.0.1 --port 8899 &
BACKEND_PID=$!
sleep 1

# 3. 启动前端
echo "[3/3] 启动前端 (port 5173)..."
cd "$DIR/frontend"
npx vite --host 127.0.0.1 --port 5173 &
FRONTEND_PID=$!

# 4. 等待前端就绪后自动打开浏览器
sleep 2
if command -v open &>/dev/null; then
  echo ""
  echo "正在打开浏览器..."
  open "$URL"
fi

echo ""
echo "============================="
echo "  后端:  http://127.0.0.1:8899/docs"
echo "  前端:  $URL"
echo "  Ctrl+C 停止所有服务"
echo "============================="

wait
