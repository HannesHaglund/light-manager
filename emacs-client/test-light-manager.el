(add-to-list 'load-path ".")
(require 'light-manager)

(setq lm-python-path "~/Documents/code/python/light-manager/client/light_manager.py")
(setq lm-helper-python-path "/home/hagge/Documents/code/python/light-manager/emacs-client/loop.py")
(setq lm-config-path "/home/hagge/Documents/code/python/light-manager/client/test_config.conf")
(setq lm-python-bin "python3 ")

(lm-run "a")
