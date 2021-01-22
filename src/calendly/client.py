import logging
from typing import Optional
from typing_extensions import Literal
from enum import Enum

import requests

from src.calendly import exceptions

logger = logging.getLogger('calendly_client')


class EventStatus(Enum):
    ACTIVE: str = 'active'
    CANCELED: str = 'canceled'


class CalendlyClient(object):
    API_URL = 'https://api.calendly.com'
    AUTH_URL = 'https://auth.calendly.com'
    CONTENT_TYPE = 'application/json'

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        client=requests,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.request = client
        self.session = client.session()
        self.session.headers.update(
            {
                'Content-Type': self.CONTENT_TYPE,
            },
        )
        self.session.headers.update(
            {
                'Authorization': 'Bearer {access_token}'.format(
                    access_token=access_token,
                ),
            },
        )

    def get_current_user(self):
        response = self.session.get(
            '{api_url}/users/me'.format(
                api_url=self.API_URL,
            ),
        )
        return self._process_response(response)

    def get_user(
        self,
        user_uuid: str,
    ):
        response = self.session.get(
            '{api_url}/users/{uuid}'.format(
                api_url=self.API_URL,
                uuid=user_uuid,
            ),
        )
        return self._process_response(response)

    def list_user_event_types(
        self,
        user_uri: str,
        sort: str = 'name:asc',
        count: int = 20,
        page_token: Optional[str] = None,
    ):
        query_string = {
            'user': user_uri,
            'sort': sort,
            'count': count,
        }
        if page_token:
            query_string['page_token'] = page_token
        response = self.session.get(
            '{api_url}/event_types'.format(
                api_url=self.API_URL,
            ),
            params=query_string,
        )
        return self._process_response(response)

    def get_event_type(self, event_uuid):
        response = self.session.get(
            '{api_url}/event_types/{uuid}'.format(
                api_url=self.API_URL,
                uuid=event_uuid,
            ),
        )
        return self._process_response(response)

    def list_events(
        self,
        count: int = 20,
        sort: str = 'start_time:asc',
        invitee_email: Optional[str] = None,
        max_start_time: Optional[str] = None,
        min_start_time: Optional[str] = None,
        organization_uri: Optional[str] = None,
        page_token: Optional[str] = None,
        status: Optional[Literal['active', 'canceled']] = None,
        user_uri: Optional[str] = None,
    ):
        query_string = {
            'count': count,
            'sort': sort,
        }
        if invitee_email:
            query_string['invitee_email'] = invitee_email
        if max_start_time:
            query_string['max_start_time'] = max_start_time
        if min_start_time:
            query_string['min_start_time'] = min_start_time
        if organization_uri:
            query_string['organization'] = organization_uri
        if page_token:
            query_string['page_token'] = page_token
        if status:
            query_string['status'] = status
        if user_uri:
            query_string['user'] = user_uri

        response = self.session.get(
            '{api_url}/scheduled_events'.format(
                api_url=self.API_URL,
            ),
            params=query_string,
        )
        return self._process_response(response)

    def _process_response(self, response):

        if response.status_code == requests.codes.ok:
            return response.json()

        if response.status_code == requests.codes.bad_request:
            raise exceptions.BadRequestException()

        if response.status_code == requests.codes.unauthorized:
            raise exceptions.UnauthorizedException()

        if response.status_code == requests.codes.forbidden:
            raise exceptions.ForbiddenException()

        if response.status_code == requests.codes.not_found:
            raise exceptions.NotFoundException()

        if response.status_code == requests.codes.internal_server_error:
            raise exceptions.InternalServerException()

        raise exceptions.UnknownException()

    def renew_with_refresh_token(
        self,
        refresh_token: str,
    ):
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
        }
        response = self.request.post(
            '{base_auth_url}/oauth/token'.format(
                base_auth_url=self.AUTH_URL,
            ),
            json=payload,
            headers={
                'Content-Type': self.CONTENT_TYPE,
            },
        )
        if response.status_code != requests.codes.ok:
            raise exceptions.RefreshTokenException

        body_response: dict = response.json()
        self.session.headers.update(
            {
                'Authorization': 'Bearer {access_token}'.format(
                    access_token=body_response.get('access_token'),
                ),
            },
        )
        return body_response.get('refresh_token')
