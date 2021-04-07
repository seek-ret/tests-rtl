from box import Box


def add_auth_in_headers(*, auth_type: str, auth_data: Box):
    """
    Add authorization data to the tavern request headers.

    :param auth_type: Type of authorization method.
    :param auth_data: Data consumed by the authorization method.
    """

    if auth_type == 'bearer':
        return Box({'Authorization': f"Bearer {auth_data.token}"})
    if auth_type == 'header':
        return Box(auth_data)

    raise RuntimeError(f'invalid auth type {auth_type}')
