# coding=utf-8

#
# class CustomContextMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         if 'audits_l' not in kwargs:
#             kwargs['audits_l'] = Audit.objects.filter(new_owner=self.request.user, is_complete=False,
#                                                       is_deferred='EM ANÁLISE').order_by('-created_at')
#         if 'notifications_l' not in kwargs:
#             kwargs['notifications_l'] = Notification.objects.filter(user=self.request.user, is_read=False).order_by(
#                 '-created_at')
#         return super(CustomContextMixin, self).get_context_data(**kwargs)
#
#
# class UserContextMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         if 'audits_for_user' not in kwargs:
#             kwargs['audits_for_user'] = Audit.objects.filter(donor=self.request.user,
#                                                              is_deferred='EM ANÁLISE').order_by('-created_at')
#         return super(UserContextMixin, self).get_context_data(**kwargs)
