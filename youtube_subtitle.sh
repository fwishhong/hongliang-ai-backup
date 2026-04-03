#!/bin/bash
# YouTube 字幕读取器 - 使用 MCP server
cd ~/clawd/mcp-server-youtube-transcript

# 从 URL 提取 video ID
URL="$1"
if [[ $URL == *"v="* ]]; then
  VIDEO_ID=$(echo "$URL" | sed 's/.*v=\([^&]*\).*/\1/')
elif [[ $URL == *"youtu.be/"* ]]; then
  VIDEO_ID=$(echo "$URL" | sed 's/.*youtu.be\/\([^?]*\).*/\1/')
else
  VIDEO_ID="$URL"
fi

echo "Fetching subtitles for: $VIDEO_ID"

node --input-type=module -e "
import { getSubtitles } from './dist/youtube-fetcher.js';
const result = await getSubtitles({ videoID: '$VIDEO_ID', lang: 'en' });
console.log('=== Video ===');
console.log('Lines:', result.lines.length);
console.log('');
console.log('=== Transcript ===');
result.lines.forEach(line => {
  console.log(line.text);
});
" 2>&1
