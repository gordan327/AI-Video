from ai_video.cli import create_parser


def test_cli_accepts_config_option():
    parser = create_parser()

    args = parser.parse_args(
        ["--config", "config/config.yaml"]
    )

    assert args.config == "config/config.yaml"