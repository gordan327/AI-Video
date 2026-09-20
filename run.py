# 強制在最外層進入點宣告所有子模組，讓 PyInstaller 絕對無法漏掉
import ai_video.detector.scrfd
import ai_video.renderer.blur
import ai_video.renderer.pixelate
import ai_video.renderer.solid
import ai_video.image.image_processor
import ai_video.gui.controller
import ai_video.gui.main_window

from ai_video.gui.app import main

if __name__ == "__main__":
    main()