#!/usr/bin/env bash

# Defines
SCRIPT=$(readlink -f "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
TARGET_REPO="git@github.com:FutaGuard/LowTechFilter.git"
TARGET_REPO_FOLDER="LowTechFilter"
FILENAME="hosts.txt"
NEW_DOMAIN="$1"

function usage() {
  echo -e "Provide the new domain you want to add\n"
  echo -e "Usage:"
  echo -e "  $SCRIPT <new_domain>"
  exit 255
}

function check_parameter() {
  if [ -z "$NEW_DOMAIN" ]; then
    usage
  else
    echo "Adding domain: $NEW_DOMAIN"
    update_repo
    insert_new_domain
  fi
}

function into_repo_folder() {
  cd "$SCRIPT_PATH/$TARGET_REPO_FOLDER" || exit 2
}

function update_repo() {
  cd "$SCRIPT_PATH" || exit 2

  if [ -d "$TARGET_REPO_FOLDER" ]; then
    rm "$TARGET_REPO_FOLDER" -rf
  fi
  git clone $TARGET_REPO $TARGET_REPO_FOLDER || git_failed
  into_repo_folder
}

function git_failed() {
  echo -e "Hey, it seems I don't have correct permission to act with GitHub."
  echo -e "That is, I can't get/push origin data from GitHub."
  echo -e "See https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey for more info."
  exit 1
}

function insert_new_domain() {
  into_repo_folder
  git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git config --local user.name "github-actions[bot]"

  LINE_NUM="$(grep -ni "! 假冒政府網站詐騙" $FILENAME | cut -d ':' -f1)"
  sed -i "$(bc <<<"$LINE_NUM+1") i ||$NEW_DOMAIN^" $FILENAME

  git commit -a -m "🤖 Telegram 群組推送"
  git push

  echo "Done!"
  exit 0
}

# https://serverfault.com/a/667997
if [ ! -n "$(grep "^github.com " ~/.ssh/known_hosts)" ]; then
  ssh-keyscan github.com 2 >>~/.ssh/known_hosts >/dev/null
fi

check_parameter
