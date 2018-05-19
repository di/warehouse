# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from collections import defaultdict
#
#from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import Authenticated
from pyramid.view import view_config
#from sqlalchemy import func
#from sqlalchemy.orm.exc import NoResultFound
#
#from warehouse.accounts.interfaces import IUserService
#from warehouse.accounts.models import User, Email
#from warehouse.accounts.views import logout
#from warehouse.email import (
#    send_account_deletion_email, send_added_as_collaborator_email,
#    send_collaborator_added_email, send_email_verification_email,
#    send_password_change_email, send_primary_email_change_email
#)
#from warehouse.manage.forms import (
#    AddEmailForm, ChangePasswordForm, CreateRoleForm, ChangeRoleForm,
#    SaveAccountForm,
#)
from warehouse.packaging.models import Project
#from warehouse.packaging.models import (
#    File, JournalEntry, Project, Release, Role,
#)
#from warehouse.utils.project import (
#    confirm_project,
#    destroy_docs,
#    remove_project,
#)


@view_config(
    route_name="support.flag-project",
    effective_principals=Authenticated,
    renderer="support/flag-project.html",
    require_csrf=True,
    require_methods=False,
    uses_session=True,
)
def flag_project(project, request):
    if request.method == "POST":
        # TODO check if this user is spamming us


    return {
        'project': project,
    }
