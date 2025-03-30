

class Permission:
    def is_logined(self, request):
        return (
            request.state.user
            and request.state.user.id
        )

    def has_perm(self, request):
        pass


class IsLogined(Permission):
    def has_perm(self, request):
        return self.is_logined(request)


class IsSuperAdmin(Permission):
    def has_perm(self, request):
        return self.is_logined(request) and request.state.user.is_superuser


class IsActive(Permission):
    def has_perm(self, request):
        return self.is_logined(request) and request.state.user.is_active
