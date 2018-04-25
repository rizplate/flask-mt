from flask_allows import Allows, Requirement
from flask import abort, g


allows = Allows(identity_loader=lambda: g.current_user)


class UserRequirementMixin(object):
    def is_profile_owner(self, identity, request):
        return identity.id == request.view_args['id']

    def fulfill(self, identity, request):
        return self.is_profile_owner(identity, request)


class CanUpdateProfile(UserRequirementMixin, Requirement):
    pass


class CanDeleteProfile(UserRequirementMixin, Requirement):
    pass


class CanCreatePost(UserRequirementMixin, Requirement):
    def fulfill(self, identity, request):
        return self.is_profile_owner(identity, request) and \
               self.is_owner_id_in_data(identity, request)

    def is_owner_id_in_data(self, identity, request):
        data = request.get_json() or {}
        if 'user_id' not in data:
            abort(400, 'must include user_id field')
        return identity.id == data['user_id']
