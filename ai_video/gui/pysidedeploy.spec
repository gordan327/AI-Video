[app]

# ai-video desktop application title
title = AI-Video

# the project root is the ai-video repository root.
project_dir = ../../..

# source file entry point, relative to project_dir.
input_file = app.py

# directory where the generated application is written.
exec_directory = dist

# optional qt project file.
project_file = 

# temporary default icon supplied by pyside6.
icon = /Users/xieguoqing/AI-Video/.venv/lib/python3.14/site-packages/PySide6/scripts/deploy_lib/pyside_icon.icns

[python]

# python interpreter used for packaging.
python_path = /Users/xieguoqing/AI-Video/.venv/bin/python

# nuitka version used by pyside6-deploy.
packages = Nuitka==4.0

# android-only dependencies.
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# ai-video currently does not use qml.
qml_files = 

# no excluded qml plugins.
excluded_qml_plugins = 

# qt modules required by the desktop gui.
modules = Core,DBus,Gui,Widgets

# qt plugins included in the application bundle.
plugins = accessiblebridge,generic,iconengines,imageformats,platforminputcontexts,platforms,platforms/darwin,platformthemes,styles

[android]
wheel_pyside = 
wheel_shiboken = 
plugins = 

[nuitka]

# no macos permissions are required yet.
macos.permissions = 

# macos produces a standalone .app bundle.
mode = standalone

# keep the first prototype build simple and diagnosable.
extra_args = --noinclude-qt-translations --include-module=scipy._external.array_api_compat.numpy.fft --include-data-dir=src/ai_video/config=ai_video/config

[buildozer]
mode = debug
recipe_dir = 
jars_dir = 
ndk_path = 
sdk_path = 
local_libs = 
arch = 

