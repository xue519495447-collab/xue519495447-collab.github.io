#!/bin/bash
# 视频处理脚本：remux faststart / 铁三角重编码 / hero 预告 / 抽帧缩略图
set -u
RAW="C:/Users/xue/.zcode/workspace/default/portfolio/raw"
OUT="C:/Users/xue/.zcode/workspace/default/portfolio/videos"
AST="C:/Users/xue/.zcode/workspace/default/portfolio/assets"
LOG="C:/Users/xue/.zcode/workspace/default/portfolio/_process.log"
cd "$RAW"
: > "$LOG"

# 顺序 = 作品编号（对应用户清单 1-13）
declare -a NAMES=(
  "冰箱贴" "防水包" "京东外卖" "魔术布" "千岛湖快闪"
  "手机防水袋" "铁三角" "线下课（终）" "行李牌" "宣传片"
  "一个人拍vlog" "真人声音4" "职场故事2.0"
)

echo "=== [$(date +%T)] 开始 remux ===" >> "$LOG"
i=0
for name in "${NAMES[@]}"; do
  i=$((i+1))
  nn=$(printf "%02d" $i)
  src="$name.mp4"
  # 读分辨率判断横竖
  wh=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$src")
  w=${wh%x*}; h=${wh#*x}
  orient="v"   # 方形/竖屏
  [ "$w" -gt "$h" ] && orient="h"
  echo "[$nn] $name ${wh} ($orient)" >> "$LOG"

  # 1) 卡片缩略图 800x500
  ffmpeg -y -loglevel error -ss 1.5 -i "$src" -frames:v 1 \
    -vf "scale=800:500:force_original_aspect_ratio=increase,crop=800:500" -q:v 3 \
    "$AST/thumb-$nn.jpg" >> "$LOG" 2>&1

  # 2) 播放器海报（保持原比例）
  if [ "$orient" = "h" ]; then
    ffmpeg -y -loglevel error -ss 1.5 -i "$src" -frames:v 1 -vf "scale=960:-2" -q:v 3 \
      "$AST/poster-$nn.jpg" >> "$LOG" 2>&1
  else
    ffmpeg -y -loglevel error -ss 1.5 -i "$src" -frames:v 1 -vf "scale=540:-2" -q:v 3 \
      "$AST/poster-$nn.jpg" >> "$LOG" 2>&1
  fi

  # 3) 成品视频：铁三角重编码两遍，其余无损 remux + faststart
  if [ "$name" = "铁三角" ]; then
    echo "[$nn] 重编码 900kbps 两遍..." >> "$LOG"
    ffmpeg -y -loglevel error -i "$src" -c:v libx264 -b:v 900k -maxrate 1350k -bufsize 2700k \
      -preset medium -pass 1 -an -f null /dev/null >> "$LOG" 2>&1
    ffmpeg -y -loglevel error -i "$src" -c:v libx264 -b:v 900k -maxrate 1350k -bufsize 2700k \
      -preset medium -pass 2 -c:a aac -b:a 128k -movflags +faststart \
      "$OUT/work-$nn.mp4" >> "$LOG" 2>&1
    rm -f ffmpeg2pass-0.log*
  else
    ffmpeg -y -loglevel error -i "$src" -c copy -movflags +faststart "$OUT/work-$nn.mp4" >> "$LOG" 2>&1
  fi
  echo "[$nn] 完成 -> $(du -m "$OUT/work-$nn.mp4" | cut -f1)MB" >> "$LOG"
done

echo "=== [$(date +%T)] hero 预告片段 ===" >> "$LOG"
ffmpeg -y -loglevel error -ss 1 -i "京东外卖.mp4"   -t 22 -c copy -movflags +faststart "$OUT/hero-1.mp4" >> "$LOG" 2>&1
ffmpeg -y -loglevel error -ss 1 -i "铁三角.mp4"     -t 22 -c copy -movflags +faststart "$OUT/hero-2.mp4" >> "$LOG" 2>&1
ffmpeg -y -loglevel error -ss 1 -i "职场故事2.0.mp4" -t 22 -c copy -movflags +faststart "$OUT/hero-3.mp4" >> "$LOG" 2>&1

echo "=== [$(date +%T)] 全部完成 ===" >> "$LOG"
ls -la "$OUT" >> "$LOG"
echo "DONE" >> "$LOG"
