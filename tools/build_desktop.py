from pathlib import Path
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SPEC_FILE = (
    PROJECT_ROOT
    / "src"
    / "ai_video"
    / "gui"
    / "pysidedeploy.spec"
)

DEPLOYMENT_DIR = (
    PROJECT_ROOT
    / "src"
    / "ai_video"
    / "gui"
    / "deployment"
)

DIST_DIR = PROJECT_ROOT / "dist"


def run_command(command: list[str]) -> None:
    """執行外部命令，失敗時立即停止建置流程。"""

    print()
    print(f"$ {' '.join(command)}")
    print()

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
    )


def check_environment() -> None:
    """確認桌面封裝所需的基本檔案與工具存在。"""

    print("=" * 60)
    print("Check Environment")
    print("=" * 60)

    if not SPEC_FILE.exists():
        raise FileNotFoundError(
            f"PySide6 deployment spec not found: {SPEC_FILE}"
        )

    if shutil.which("pyside6-deploy") is None:
        raise RuntimeError(
            "pyside6-deploy was not found in the current environment."
        )

    print(f"Project root   : {PROJECT_ROOT}")
    print(f"Spec file      : {SPEC_FILE}")
    print(f"Deployment dir : {DEPLOYMENT_DIR}")
    print(f"Distribution   : {DIST_DIR}")


def clean_previous_build() -> None:
    """清除先前的桌面封裝產物。"""

    print()
    print("=" * 60)
    print("Clean Previous Build")
    print("=" * 60)

    if DEPLOYMENT_DIR.exists():
        print(f"Removing: {DEPLOYMENT_DIR}")
        shutil.rmtree(DEPLOYMENT_DIR)
    else:
        print("No previous deployment directory found.")

    if DIST_DIR.exists():
        for app_bundle in DIST_DIR.glob("*.app"):
            print(f"Removing: {app_bundle}")
            shutil.rmtree(app_bundle)
    else:
        DIST_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created: {DIST_DIR}")


def run_tests() -> None:
    """執行完整測試套件。"""

    print()
    print("=" * 60)
    print("Run Tests")
    print("=" * 60)

    run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
        ]
    )


def run_pyside6_deploy() -> None:
    """使用 pyside6-deploy 建立 macOS application bundle。"""

    print()
    print("=" * 60)
    print("Build Desktop Application")
    print("=" * 60)

    run_command(
        [
            "pyside6-deploy",
            "-c",
            str(SPEC_FILE),
            "--force",
        ]
    )


def find_generated_bundle() -> Path:
    """尋找 pyside6-deploy 產生的 .app bundle。"""

    if not DEPLOYMENT_DIR.exists():
        raise FileNotFoundError(
            "Deployment directory was not created: "
            f"{DEPLOYMENT_DIR}"
        )

    app_bundles = sorted(DEPLOYMENT_DIR.glob("*.app"))

    if not app_bundles:
        raise FileNotFoundError(
            "No macOS application bundle was found in: "
            f"{DEPLOYMENT_DIR}"
        )

    if len(app_bundles) > 1:
        names = ", ".join(bundle.name for bundle in app_bundles)
        raise RuntimeError(
            "Multiple application bundles were found in "
            f"{DEPLOYMENT_DIR}: {names}"
        )

    return app_bundles[0]


def copy_bundle_to_dist(source_bundle: Path) -> Path:
    """將產生的 .app bundle 複製到 dist 目錄。"""

    print()
    print("=" * 60)
    print("Copy Bundle to Distribution Directory")
    print("=" * 60)

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    destination_bundle = DIST_DIR / source_bundle.name

    if destination_bundle.exists():
        shutil.rmtree(destination_bundle)

    print(f"Source      : {source_bundle}")
    print(f"Destination : {destination_bundle}")

    shutil.copytree(
        source_bundle,
        destination_bundle,
        symlinks=True,
    )

    return destination_bundle


def verify_bundle(bundle_path: Path) -> None:
    """確認最終 application bundle 已成功建立。"""

    print()
    print("=" * 60)
    print("Verify Desktop Bundle")
    print("=" * 60)

    if not bundle_path.exists():
        raise FileNotFoundError(
            f"Application bundle does not exist: {bundle_path}"
        )

    if not bundle_path.is_dir():
        raise RuntimeError(
            f"Application bundle is not a directory: {bundle_path}"
        )

    contents_directory = bundle_path / "Contents"

    if not contents_directory.exists():
        raise RuntimeError(
            "Invalid macOS application bundle. "
            f"Missing directory: {contents_directory}"
        )

    print(f"Application bundle verified: {bundle_path}")


def main() -> int:
    """執行完整桌面版建置流程。"""

    try:
        check_environment()
        clean_previous_build()
        run_tests()
        run_pyside6_deploy()

        generated_bundle = find_generated_bundle()
        distribution_bundle = copy_bundle_to_dist(
            generated_bundle
        )

        verify_bundle(distribution_bundle)

    except (
        FileNotFoundError,
        RuntimeError,
        subprocess.CalledProcessError,
    ) as error:
        print()
        print("=" * 60)
        print("Desktop Build Failed")
        print("=" * 60)
        print(error)

        return 1

    print()
    print("=" * 60)
    print("Desktop Build Completed")
    print("=" * 60)
    print(f"Application bundle: {distribution_bundle}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())