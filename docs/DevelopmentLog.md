# Development Log

## 2026-07-01

### Version 0.1 - Project Initialization

完成項目：

- 建立 AI-Video 專案目錄
- 建立 Python 虛擬環境 (.venv)
- 安裝 OpenCV
- 安裝 FFmpeg
- 建立 Git Repository
- 建立 README.md
- 建立 LICENSE (MIT)
- 建立 .gitignore
- 建立 requirements.txt
- 建立 config/config.yaml

學習重點：

- Git Repository 的概念
- .gitignore 的用途
- README 的角色
- 專案文件管理
- 使用 VS Code 管理專案

下一步：

- 建立 SRS（需求規格）
- 建立 Roadmap
- 完成第一次 Git Commit
- 開始開發 Video Reader

🎉 第一個 Git Commit 完成。

Commit Message：

Initialize project structure

## 設計決策

本專案採用 Processor 架構。

main.py 不直接實作任何影片處理流程，而是負責啟動程式及載入設定。

所有影片處理流程統一由 processor.py 協調，再依序呼叫各功能模組。

這樣的設計可以降低 main.py 的複雜度，也方便未來增加 GUI、命令列、API 等不同的操作介面，而不必修改核心處理流程。

## 2026-07-03

### Milestone 0.3：VideoReader 完成

完成 VideoReader 類別，可支援：

- 開啟影片
- 檢查影片是否存在
- 取得 FPS
- 取得解析度
- 取得總影格數
- 計算影片長度
- 逐格讀取 Frame（read）
- 關閉影片

使用 main.py 成功測試 MP4 影片。

## 2026-07-03

### Milestone 0.4：Video Processing Pipeline 完成。

完成  類別VideoProcessor:

- 確認 Pipeline 已經打通

再次使用 main.py 成功測試 MP4 影片。

