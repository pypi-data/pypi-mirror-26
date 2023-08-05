from .provider_base import ProviderBase


class ProviderGenius(ProviderBase):
    def get_name(self):
        return "Genius"

    def get_url(self, title, artist, album):
        return 'https://genius.com/{}-{}-lyrics'.format(self.encode(artist),
                                                        self.encode(title))

    def get_xpath(self, title, artist, album):
        return '//div[@class="lyrics"]//text()'

    def get_regex(self, title, artist, album):
        return ''

    def get_node_separator(self):
        return ''

    def encode(self, param):
        param = (
            param
            .lower()
            .replace(' ', '-')
            .replace('(', '')
            .replace(')', '')
            .replace('.', '')
            .replace('[', '')
            .replace(']', '')
            .replace('/', '')
            .replace('?', '')
            .replace('!', '')
            .replace("'", '')
        )

        return super().encode(param)
