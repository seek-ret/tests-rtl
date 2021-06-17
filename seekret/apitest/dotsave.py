from box import Box
from tavern.util.dict_util import recurse_access_key

from seekret.apitest._createleaf import create_leaf


def dots_save(response, *, headers: dict = None, body: dict = None):
    """
    Tavern extension function that saves dotted keys as objects.

    Consider the following example::

        stages:
          - name: Stage 1
            request:
                ...
            response:
                ...
                save:
                    $ext:
                        function: seekret.apitest:dots_save
                        extra_kwargs:
                            body:
                                user.id: id
          - name Stage 2
            request:
                ...
                json:
                    user: !force_format_include "{user}"
                ...

    The second request will have the following body::

        {
            "user": {
                "id": ...
            }
        }
    """

    saved = Box()
    for save_block, response_data in [(headers, response.headers),
                                      (body, response.json())]:
        if not save_block:
            continue

        for save_as, joined_key in save_block.items():
            saved.merge_update(
                create_leaf(save_as,
                            recurse_access_key(response_data, joined_key)))

    return saved.to_dict()
