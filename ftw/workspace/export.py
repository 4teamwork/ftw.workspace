from Acquisition._Acquisition import aq_parent, aq_base
from ftw.workspace import arbeitsraumMessageFactory as _
from Products.CMFCore.utils import getToolByName
import StringIO
import xlsxwriter


ROLES_WHITE_LIST = ['Owner']


def format_date(date):
    if not date:
        return ''
    if date.year() <= 1900:
        return ''
    else:
        return date.strftime('%d.%m.%Y %H:%M')


def fullname(context, uid):
    member = context.portal_membership.getMemberById(uid)
    if member:
        fullname = member.getProperty('fullname', member.getId())
        if fullname:
            return fullname
        return member.getId()
    return uid


def get_participants(context):
    """Get the participants (which are local_roles).
    """
    mtool = getToolByName(context, 'portal_membership')
    users = []

    for userid, roles in get_roles_settings(context):

        member = mtool.getMemberById(userid)

        # skip groups
        if member is not None:
            email = member.getProperty('email', '')
            name = member.getProperty('fullname', '')

            all_roles = roles.keys()
            inherited_roles = [r for r, v in roles.items()
                               if v]

            item = dict(
                userid=userid,
                roles=all_roles,
                inherited_roles=inherited_roles)

            if name:
                item['name'] = name.decode('utf-8')
            else:
                item['name'] = userid.decode('utf-8')

            if email:
                item['email'] = email.decode('utf-8')
            else:
                item['email'] = ''

            if item.get('roles') or item.get('inherited_roles'):
                users.append(item)

    users.sort(key=lambda item: item['name'].lower())
    return users


def get_roles_settings(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    result = {}

    def get_roles(context, acquired=False):
        for userid, roles in context.get_local_roles():
            roles = list(roles)
            if 'Owner' in roles and acquired:
                roles.remove('Owner')

            if userid not in result:
                result[userid] = dict((role, acquired) for role in roles)
            else:
                current_roles = result[userid]
                for role in roles:
                    if role not in current_roles:
                        current_roles[role] = acquired

        parent = aq_parent(context)
        if parent != portal and inherited(context):
            get_roles(parent, acquired=True)

    get_roles(context)
    result = list(result.items())
    return result


def inherited(context):
    """Return True if local roles are inherited on the context.
    """
    return not bool(
        getattr(aq_base(context), '__ac_local_roles_block__', None))


def get_header(context):
    return [
        context.translate(
            _(u'export_heading_user_id', default=u'User ID')),
        context.translate(
            _(u'export_heading_full_name', default=u'Full name')),
        context.translate(
            _(u'export_heading_email', default=u'E-Mail')),
        context.translate(
            _(u'export_heading_roles', default=u'Roles')),
    ]


def get_data(context):
    data = []

    for participant in get_participants(context):
        row = [
            participant['userid'].encode('utf-8'),
            participant['name'].encode('utf-8'),
            participant['email'].encode('utf-8'),
            ', '.join(participant['roles']),
        ]
        data.append(row)

    return data


def create_xlsx(header=None, data=None):
    if not header:
        header = []
    if not data:
        data = []

    # Create an in-memory output file for the new workbook.
    output = StringIO.StringIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' constructor option to True.
    workbook = xlsxwriter.Workbook(output, {'in_memory': False})
    worksheet = workbook.add_worksheet()

    # Add a bold format for the header.
    bold = workbook.add_format({'bold': True})

    # Write the header.
    for index, item in enumerate(header):
        worksheet.write(0, index, item, bold)

    # Write the data (which is a nested list).
    for row_index, row_item in enumerate(data):
        for column_index, column_item in enumerate(row_item):
            worksheet.write_string(
                row_index+1, column_index, column_item.decode('utf-8'))

    # Set the auto filter only if there is something to filter.
    if header and data:
        worksheet.autofilter(0, 0, len(data)+1, len(data[0])-1)

    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    return output
