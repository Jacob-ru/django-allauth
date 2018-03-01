import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import VKProvider


USER_FIELDS = ['first_name',
               'last_name',
               'nickname',
               'screen_name',
               'sex',
               'bdate',
               'city',
               'country',
               'timezone',
               'photo',
               'photo_medium',
               'photo_big',
               'has_mobile',
               'contacts',
               'education',
               'online',
               'counters',
               'relation',
               'last_seen',
               'activity',
               'universities']


class VKOAuth2Adapter(OAuth2Adapter):
    provider_id = VKProvider.id
    access_token_url = 'https://oauth.vk.com/access_token'
    authorize_url = 'https://oauth.vk.com/authorize'
    profile_url = 'https://api.vk.com/method/users.get'

    def complete_login(self, request, app, token, **kwargs):
        uid = kwargs['response']['user_id']
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'fields': ','.join(USER_FIELDS),
                                    'user_ids': uid,
                                    'v': 3})
        resp.raise_for_status()
        extra_data = resp.json()['response'][0]
        email = kwargs['response'].get('email')
        if email:
            extra_data['email'] = email
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(VKOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKOAuth2Adapter)
