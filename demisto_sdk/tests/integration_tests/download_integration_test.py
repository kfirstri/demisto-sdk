from os.path import join

import pytest
from click.testing import CliRunner
from demisto_sdk.__main__ import main
from demisto_sdk.commands.common.git_tools import git_path
from demisto_sdk.commands.download.tests.downloader_test import Environment

DOWNLOAD_COMMAND = "download"
DEMISTO_SDK_PATH = join(git_path(), "demisto_sdk")


@pytest.fixture
def demisto_client(mocker):
    mocker.patch(
        "demisto_sdk.commands.download.downloader.demisto_client",
        return_valure="object"
    )
    with open('demisto_sdk/tests/test_files/download_command/demisto_api_response', 'r') as f:
        api_response = f.read()
    mocker.patch(
        "demisto_sdk.commands.download.downloader.demisto_client.generic_request_func",
        return_value=(api_response, None, None)
    )


def test_integration_download_no_force(demisto_client, tmp_path):
    """
    Given
    - playbook & script exist in the output pack path.

    When
    - Running demisto-sdk download command.

    Then
    - Ensure no download has been made.
    - Ensure force msg is printed.
    """
    env = Environment(tmp_path)
    pack_path = join(DEMISTO_SDK_PATH, env.PACK_INSTANCE_PATH)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(main, [DOWNLOAD_COMMAND, "-o", pack_path, "-i", "TestScript", "-i", "DummyPlaybook"])
    assert "Demisto instance: Enumerating objects: 2, done." in result.output
    assert "Demisto instance: Receiving objects: 100% (2/2), done." in result.output
    assert "Failed to download the following files:" in result.output
    assert "FILE NAME      REASON" in result.output
    assert "-------------  ------------------" in result.output
    assert "TestScript     File already exist" in result.output
    assert "DummyPlaybook  File already exist" in result.output
    assert "To merge existing files use the download command with -f." in result.output
    assert result.exit_code == 0
    assert not result.stderr
    assert not result.exception


def test_integration_download_with_force(demisto_client, tmp_path):
    """
    Given
    - playbook & script exist in the output pack path.

    When
    - Running demisto-sdk download command.

    Then
    - Ensure download has been made successfully.
    """
    env = Environment(tmp_path)
    pack_path = join(DEMISTO_SDK_PATH, env.PACK_INSTANCE_PATH)
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(main, [DOWNLOAD_COMMAND, "-o", pack_path, "-i", "TestScript", "-i", "DummyPlaybook", "-f"])
    assert "Demisto instance: Enumerating objects: 2, done." in result.output
    assert "Demisto instance: Receiving objects: 100% (2/2), done." in result.output
    assert '- Merged Script "TestScript"' in result.output
    assert '- Merged Playbook "DummyPlaybook"' in result.output
    assert "2 files merged." in result.output
    assert result.exit_code == 0
    assert not result.stderr
    assert not result.exception


def test_integration_download_list_files(demisto_client):
    """
    Given
    - lf flag to list all available content items.

    When
    - Running demisto-sdk download command.

    Then
    - Ensure list files has been made successfully.
    """
    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(main, [DOWNLOAD_COMMAND, "-lf"])
    assert "The following files are available to be downloaded from Demisto instance:" in result.output
    assert "FILE NAME                          FILE TYPE" in result.output
    assert "---------------------------------  ------------" in result.output
    assert "Handle Hello World Alert Test      TestPlaybook" in result.output
    assert "CommonServerUserPython             Script" in result.output
    assert "MSGraph_DeviceManagement_Test      TestPlaybook" in result.output
    assert "CommonUserServer                   Script" in result.output
    assert "DummyPlaybook                      Playbook" in result.output
    assert "Test Integration                   Integration" in result.output
    assert "TestScript                         Script" in result.output
    assert "Symantec Data Loss Prevention      Integration" in result.output
    assert "FormattingPerformance - Test       TestPlaybook" in result.output
    assert "CommonServerUserPowerShell         Script" in result.output
    assert "Microsoft Graph Device Management  Integration" in result.output
    assert "FormattingPerformance              Script" in result.output
    assert "Protectwise-Test                   TestPlaybook" in result.output
    assert "guy                                Playbook" in result.output
    assert result.exit_code == 0
    assert not result.stderr
    assert not result.exception
