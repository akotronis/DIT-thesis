import streamlit as st

import utils as utl
import services as srv
import utils as utl
from views.groups import vw_services as vw_srv


utl.display_state_messages()

page = utl.centered_page_of(.8)
with page:
    st.header(f'Invitations Page', divider=True)
    sent_invitations = srv.get_api().get_invitations('host')[-1].get('results', []) or []
    sent_column_widths = [.3, .1, .4, .2]
    with st.expander('**Invitations sent (host)**', icon=':material/outgoing_mail:'):
        if not sent_invitations:
            st.container(height=30, border=False)
            st.write('No invitations sent')
        else:
            with st.container(border=False):
                sent_columns = ['GUEST', 'GROUP', 'DATETIME', 'STATUS']
                header = st.container(border=True).columns(sent_column_widths, vertical_alignment='center')
                for i, item in enumerate(sent_columns):
                    header[i].markdown(f'**{item}**')
            with st.container(height=200, border=False):
                for inv in sent_invitations:
                    id_ = inv.get('id')
                    row = st.container(border=True).columns(sent_column_widths, vertical_alignment='center')
                    row[0].write(f"({id_}) - {inv.get('guest')}")
                    row[1].write(inv.get('group', {}).get('name'))
                    row[2].write(utl.format_timestamp(inv.get('created_at')))
                    row[3].write(inv.get('status'))

    st.container(height=30, border=False)

    received_invitations = srv.get_api().get_invitations('guest')[-1].get('results', []) or []
    received_column_widths = [.3, .1, .3, .2, .1]
    with st.expander('**Invitations received (guest)**', icon=':material/mail:'):
        if not received_invitations:
            st.container(height=30, border=False)
            st.write('No invitations received')
        else:
            with st.container(border=False):
                received_columns = ['HOST', 'GROUP', 'DATETIME', 'STATUS', 'ACTION']
                header = st.container(border=True).columns(received_column_widths, vertical_alignment='center')
                for i, item in enumerate(received_columns):
                    header[i].markdown(f'**{item.upper()}**')
            with st.container(height=200, border=False):
                for inv in received_invitations:
                    id_ = inv.get('id')
                    row = st.container(border=True).columns(received_column_widths, vertical_alignment='center')
                    row[0].write(f"({id_}) - {inv.get('host')}")
                    group_name = inv.get('group', {}).get('name')
                    row[1].write(group_name)
                    row[2].write(utl.format_timestamp(inv.get('created_at')))
                    status = inv.get('status')
                    disabled = status != 'PENDING'
                    row[3].write(status)
                    help_disabled_kwargs = {'disabled':disabled, **({'help':'Accept/Reject Invitation'} if not disabled else {})}
                    row[4].button('', **help_disabled_kwargs, icon=':material/arrow_right_alt:',
                                use_container_width=True, on_click=vw_srv.respond_to_invitation,
                                key=f'inv-{id_}-action', kwargs={'id_':id_, 'group_name': group_name}, type='primary')