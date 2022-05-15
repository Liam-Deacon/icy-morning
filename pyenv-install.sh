#! /bin/bash
which pyenv || \
curl https://pyenv.run | bash && \
cat >> ~/.bashrc << EOF
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
EOF
