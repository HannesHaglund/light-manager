(require 'ansi-color)

;; Config these outside of this file
;; (setq lm-python-path "~/Documents/code/python/light-manager/client/light_manager.py")
;; (setq lm-helper-python-path "/home/hagge/Documents/code/python/light-manager/emacs-client/loop.py")
;; (setq lm-config-path "/home/hagge/Documents/code/python/light-manager/client/test_config.conf")
;; (setq lm-python-bin "python3 ")

(setq lm-buffer-name "*light-manager*")
(setq lm-last-command "a")
(unless (and (boundp 'lm-update-timer) (timerp lm-update-timer)) (setq lm-update-timer nil))
(setq lm-update-timer-how-often 5)
(setq lm-tmp nil)
(add-hook 'kill-buffer-hook 'lm-kill-buffer-hook-fun)

(defadvice display-message-or-buffer (before ansi-color activate)
  "Process ANSI color codes in light manager output."
  (let ((buf (ad-get-arg 0)))
    (and (bufferp buf)
         (string= (buffer-name buf) lm-buffer-name)
         (with-current-buffer buf
           (ansi-color-apply-on-region (point-min) (point-max))))))

(defun lm-run (key)
  (defvar light-manager-mode-map (make-keymap) "lm-mode keymap.")
  (define-key light-manager-mode-map (kbd "q") 'kill-this-buffer)
  (lm-set-local-run-key "0" light-manager-mode-map)            ; Toggle light 0-9
  (lm-set-local-run-key "1" light-manager-mode-map)
  (lm-set-local-run-key "2" light-manager-mode-map)
  (lm-set-local-run-key "3" light-manager-mode-map)
  (lm-set-local-run-key "4" light-manager-mode-map)
  (lm-set-local-run-key "5" light-manager-mode-map)
  (lm-set-local-run-key "6" light-manager-mode-map)
  (lm-set-local-run-key "7" light-manager-mode-map)
  (lm-set-local-run-key "8" light-manager-mode-map)
  (lm-set-local-run-key "9" light-manager-mode-map)
  (lm-set-local-run-key "a" light-manager-mode-map)            ; Return to auto-mode
  (lm-set-local-run-key "r" light-manager-mode-map)            ; Refresh if auto
  (define-minor-mode light-manager-mode
    "Minor mode for keybindings in lm-buffer"
    :init-value nil
    "lm-mode"
    light-manager-mode-map)
  (with-output-to-temp-buffer lm-buffer-name
    (save-window-excursion
      (setq lm-tmp (current-buffer))
      (shell-command
       (concat
        lm-python-bin
        lm-helper-python-path
        " " lm-python-path
        " " lm-config-path
        " " lm-last-command
        " " key)
       (pop-to-buffer lm-buffer-name))
      (light-manager-mode 1)
      (ansi-color-apply-on-region (point-min) (point-max)))
    ;; Afte window exucision
     (unless (string= key "r") (pop-to-buffer lm-tmp)))
  (unless lm-update-timer
    (setq lm-update-timer (run-with-timer
                           0
                           lm-update-timer-how-often
                           (lambda () (lm-run "r"))))))

(defun lm-kill-buffer-hook-fun ()
  (when (and lm-update-timer (string= lm-buffer-name (buffer-name (current-buffer))))
    (lm-kill-timer)))

(defun lm-kill-timer ()
  (when (timerp lm-update-timer)
    (cancel-timer lm-update-timer)
    (setq lm-update-timer nil)))

(defun light-manager-kill-timer ()
  (interactive)
  (lm-kill-timer))

(defun lm-set-local-run-key (keystr mode)
  (define-key mode (kbd keystr) `(lambda ()
                                 (interactive)
                                 (lm-run ,keystr)
                                 (unless (string= ,keystr "r")
                                   (setq lm-last-command ,keystr)))))

(defun light-manager ()
  (interactive)
  (lm-run "a"))


(provide 'light-manager)
