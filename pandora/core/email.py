import shutil
import webbrowser

from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend
from django.template.loader import render_to_string

# Register additional browsers if available
if shutil.which('google-chrome-beta'):
    webbrowser.register('google-chrome-beta', None, webbrowser.Chrome('google-chrome-beta'))
if shutil.which('google-chrome-unstable'):
    webbrowser.register('google-chrome-unstable', None, webbrowser.Chrome('google-chrome-unstable'))


class EmailBackend(FileBasedEmailBackend):

    def _get_filename(self):
        filename = super()._get_filename()
        self._fname = filename.replace('.log', '.html')
        return self._fname

    def write_message(self, message):
        text_message = message.body
        html_message = None

        if isinstance(message, EmailMultiAlternatives):
            for (content, mimetype) in message.alternatives:
                if mimetype == 'text/html':
                    html_message = content

        self.stream.write(render_to_string('email_debug.html', {
            'subject': message.subject,
            'full_message': message.message(),
            'text_message': text_message,
            'html_message': html_message
        }).encode('utf-8'))

    def close(self):
        super().close()
        print(f'Opening "{self._fname}" in a browser')
        webbrowser.open(f'file://{self._fname}')
