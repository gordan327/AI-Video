from ai_video.cli import create_parser


def test_cli_accepts_config_option():
    parser = create_parser()

    args = parser.parse_args(
        ["--config", "config/config.yaml"]
    )

    assert args.config == "config/config.yaml"

def test_cli_default_config_is_none():
    parser = create_parser()

    args = parser.parse_args([])

    assert args.config is None

from ai_video.cli import print_version


def test_print_version(capsys):
    print_version()

    captured = capsys.readouterr()

    assert "AI-Video" in captured.out

from ai_video.cli import main


def test_main_version_returns_zero(
    monkeypatch,
):
    monkeypatch.setattr(
        "sys.argv",
        ["ai-video", "--version"],
    )

    assert main() == 0