# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class NagiosAcknowledgements(models.Model):
    acknowledgement_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    entry_time = models.DateTimeField()
    entry_time_usec = models.IntegerField()
    acknowledgement_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    state = models.SmallIntegerField()
    author_name = models.CharField(max_length=64)
    comment_data = models.CharField(max_length=255)
    is_sticky = models.SmallIntegerField()
    persistent_comment = models.SmallIntegerField()
    notify_contacts = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_acknowledgements'


class NagiosCommands(models.Model):
    command_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    command_line = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_commands'


class NagiosCommenthistory(models.Model):
    commenthistory_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    entry_time = models.DateTimeField()
    entry_time_usec = models.IntegerField()
    comment_type = models.SmallIntegerField()
    entry_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    comment_time = models.DateTimeField()
    internal_comment_id = models.IntegerField()
    author_name = models.CharField(max_length=64)
    comment_data = models.CharField(max_length=255)
    is_persistent = models.SmallIntegerField()
    comment_source = models.SmallIntegerField()
    expires = models.SmallIntegerField()
    expiration_time = models.DateTimeField()
    deletion_time = models.DateTimeField()
    deletion_time_usec = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_commenthistory'


class NagiosComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    entry_time = models.DateTimeField()
    entry_time_usec = models.IntegerField()
    comment_type = models.SmallIntegerField()
    entry_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    comment_time = models.DateTimeField()
    internal_comment_id = models.IntegerField()
    author_name = models.CharField(max_length=64)
    comment_data = models.CharField(max_length=255)
    is_persistent = models.SmallIntegerField()
    comment_source = models.SmallIntegerField()
    expires = models.SmallIntegerField()
    expiration_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nagios_comments'


class NagiosConfigfiles(models.Model):
    configfile_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    configfile_type = models.SmallIntegerField()
    configfile_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_configfiles'


class NagiosConfigfilevariables(models.Model):
    configfilevariable_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    configfile_id = models.IntegerField()
    varname = models.CharField(max_length=64)
    varvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_configfilevariables'


class NagiosConninfo(models.Model):
    conninfo_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    agent_name = models.CharField(max_length=32)
    agent_version = models.CharField(max_length=8)
    disposition = models.CharField(max_length=16)
    connect_source = models.CharField(max_length=16)
    connect_type = models.CharField(max_length=16)
    connect_time = models.DateTimeField()
    disconnect_time = models.DateTimeField()
    last_checkin_time = models.DateTimeField()
    data_start_time = models.DateTimeField()
    data_end_time = models.DateTimeField()
    bytes_processed = models.IntegerField()
    lines_processed = models.IntegerField()
    entries_processed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_conninfo'


class NagiosContactAddresses(models.Model):
    contact_address_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    contact_id = models.IntegerField()
    address_number = models.SmallIntegerField()
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_contact_addresses'


class NagiosContactNotificationcommands(models.Model):
    contact_notificationcommand_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    contact_id = models.IntegerField()
    notification_type = models.SmallIntegerField()
    command_object_id = models.IntegerField()
    command_args = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_contact_notificationcommands'


class NagiosContactgroupMembers(models.Model):
    contactgroup_member_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    contactgroup_id = models.IntegerField()
    contact_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_contactgroup_members'


class NagiosContactgroups(models.Model):
    contactgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    contactgroup_object_id = models.IntegerField()
    alias = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_contactgroups'


class NagiosContactnotificationmethods(models.Model):
    contactnotificationmethod_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    contactnotification_id = models.IntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    command_object_id = models.IntegerField()
    command_args = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_contactnotificationmethods'


class NagiosContactnotifications(models.Model):
    contactnotification_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    notification_id = models.IntegerField()
    contact_object_id = models.IntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_contactnotifications'


class NagiosContacts(models.Model):
    contact_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    contact_object_id = models.IntegerField()
    alias = models.CharField(max_length=64)
    email_address = models.CharField(max_length=255)
    pager_address = models.CharField(max_length=64)
    host_timeperiod_object_id = models.IntegerField()
    service_timeperiod_object_id = models.IntegerField()
    host_notifications_enabled = models.SmallIntegerField()
    service_notifications_enabled = models.SmallIntegerField()
    can_submit_commands = models.SmallIntegerField()
    notify_service_recovery = models.SmallIntegerField()
    notify_service_warning = models.SmallIntegerField()
    notify_service_unknown = models.SmallIntegerField()
    notify_service_critical = models.SmallIntegerField()
    notify_service_flapping = models.SmallIntegerField()
    notify_service_downtime = models.SmallIntegerField()
    notify_host_recovery = models.SmallIntegerField()
    notify_host_down = models.SmallIntegerField()
    notify_host_unreachable = models.SmallIntegerField()
    notify_host_flapping = models.SmallIntegerField()
    notify_host_downtime = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_contacts'


class NagiosContactstatus(models.Model):
    contactstatus_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    contact_object_id = models.IntegerField(unique=True)
    status_update_time = models.DateTimeField()
    host_notifications_enabled = models.SmallIntegerField()
    service_notifications_enabled = models.SmallIntegerField()
    last_host_notification = models.DateTimeField()
    last_service_notification = models.DateTimeField()
    modified_attributes = models.IntegerField()
    modified_host_attributes = models.IntegerField()
    modified_service_attributes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_contactstatus'


class NagiosCustomvariables(models.Model):
    customvariable_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    object_id = models.IntegerField()
    config_type = models.SmallIntegerField()
    has_been_modified = models.SmallIntegerField()
    varname = models.CharField(max_length=255)
    varvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_customvariables'


class NagiosCustomvariablestatus(models.Model):
    customvariablestatus_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    object_id = models.IntegerField()
    status_update_time = models.DateTimeField()
    has_been_modified = models.SmallIntegerField()
    varname = models.CharField(max_length=255)
    varvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_customvariablestatus'


class NagiosDbversion(models.Model):
    name = models.CharField(max_length=10)
    version = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'nagios_dbversion'


class NagiosDowntimehistory(models.Model):
    downtimehistory_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    downtime_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    entry_time = models.DateTimeField()
    author_name = models.CharField(max_length=64)
    comment_data = models.CharField(max_length=255)
    internal_downtime_id = models.IntegerField()
    triggered_by_id = models.IntegerField()
    is_fixed = models.SmallIntegerField()
    duration = models.SmallIntegerField()
    scheduled_start_time = models.DateTimeField()
    scheduled_end_time = models.DateTimeField()
    was_started = models.SmallIntegerField()
    actual_start_time = models.DateTimeField()
    actual_start_time_usec = models.IntegerField()
    actual_end_time = models.DateTimeField()
    actual_end_time_usec = models.IntegerField()
    was_cancelled = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_downtimehistory'


class NagiosEventhandlers(models.Model):
    eventhandler_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    eventhandler_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    state = models.SmallIntegerField()
    state_type = models.SmallIntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    command_object_id = models.IntegerField()
    command_args = models.CharField(max_length=255)
    command_line = models.CharField(max_length=255)
    timeout = models.SmallIntegerField()
    early_timeout = models.SmallIntegerField()
    execution_time = models.FloatField()
    return_code = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()

    class Meta:
        managed = False
        db_table = 'nagios_eventhandlers'


class NagiosExternalcommands(models.Model):
    externalcommand_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    entry_time = models.DateTimeField()
    command_type = models.SmallIntegerField()
    command_name = models.CharField(max_length=128)
    command_args = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_externalcommands'


class NagiosFlappinghistory(models.Model):
    flappinghistory_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    event_time = models.DateTimeField()
    event_time_usec = models.IntegerField()
    event_type = models.SmallIntegerField()
    reason_type = models.SmallIntegerField()
    flapping_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    percent_state_change = models.FloatField()
    low_threshold = models.FloatField()
    high_threshold = models.FloatField()
    comment_time = models.DateTimeField()
    internal_comment_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_flappinghistory'


class NagiosHostContactgroups(models.Model):
    host_contactgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    host_id = models.IntegerField()
    contactgroup_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_host_contactgroups'


class NagiosHostContacts(models.Model):
    host_contact_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    host_id = models.IntegerField()
    contact_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_host_contacts'


class NagiosHostParenthosts(models.Model):
    host_parenthost_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    host_id = models.IntegerField()
    parent_host_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_host_parenthosts'


class NagiosHostchecks(models.Model):
    hostcheck_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    host_object_id = models.IntegerField()
    check_type = models.SmallIntegerField()
    is_raw_check = models.SmallIntegerField()
    current_check_attempt = models.SmallIntegerField()
    max_check_attempts = models.SmallIntegerField()
    state = models.SmallIntegerField()
    state_type = models.SmallIntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    command_object_id = models.IntegerField()
    command_args = models.CharField(max_length=255)
    command_line = models.CharField(max_length=255)
    timeout = models.SmallIntegerField()
    early_timeout = models.SmallIntegerField()
    execution_time = models.FloatField()
    latency = models.FloatField()
    return_code = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()
    perfdata = models.TextField()

    class Meta:
        managed = False
        db_table = 'nagios_hostchecks'


class NagiosHostdependencies(models.Model):
    hostdependency_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    host_object_id = models.IntegerField()
    dependent_host_object_id = models.IntegerField()
    dependency_type = models.SmallIntegerField()
    inherits_parent = models.SmallIntegerField()
    timeperiod_object_id = models.IntegerField()
    fail_on_up = models.SmallIntegerField()
    fail_on_down = models.SmallIntegerField()
    fail_on_unreachable = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hostdependencies'


class NagiosHostescalationContactgroups(models.Model):
    hostescalation_contactgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    hostescalation_id = models.IntegerField()
    contactgroup_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hostescalation_contactgroups'


class NagiosHostescalationContacts(models.Model):
    hostescalation_contact_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    hostescalation_id = models.IntegerField()
    contact_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hostescalation_contacts'


class NagiosHostescalations(models.Model):
    hostescalation_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    host_object_id = models.IntegerField()
    timeperiod_object_id = models.IntegerField()
    first_notification = models.SmallIntegerField()
    last_notification = models.SmallIntegerField()
    notification_interval = models.FloatField()
    escalate_on_recovery = models.SmallIntegerField()
    escalate_on_down = models.SmallIntegerField()
    escalate_on_unreachable = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hostescalations'


class NagiosHostgroupMembers(models.Model):
    hostgroup_member_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    hostgroup_id = models.IntegerField()
    host_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hostgroup_members'


class NagiosHostgroups(models.Model):
    hostgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    hostgroup_object_id = models.IntegerField()
    alias = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_hostgroups'


class NagiosHosts(models.Model):
    host_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    host_object_id = models.IntegerField()
    alias = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    check_command_object_id = models.IntegerField()
    check_command_args = models.CharField(max_length=255)
    eventhandler_command_object_id = models.IntegerField()
    eventhandler_command_args = models.CharField(max_length=255)
    notification_timeperiod_object_id = models.IntegerField()
    check_timeperiod_object_id = models.IntegerField()
    failure_prediction_options = models.CharField(max_length=64)
    check_interval = models.FloatField()
    retry_interval = models.FloatField()
    max_check_attempts = models.SmallIntegerField()
    first_notification_delay = models.FloatField()
    notification_interval = models.FloatField()
    notify_on_down = models.SmallIntegerField()
    notify_on_unreachable = models.SmallIntegerField()
    notify_on_recovery = models.SmallIntegerField()
    notify_on_flapping = models.SmallIntegerField()
    notify_on_downtime = models.SmallIntegerField()
    stalk_on_up = models.SmallIntegerField()
    stalk_on_down = models.SmallIntegerField()
    stalk_on_unreachable = models.SmallIntegerField()
    flap_detection_enabled = models.SmallIntegerField()
    flap_detection_on_up = models.SmallIntegerField()
    flap_detection_on_down = models.SmallIntegerField()
    flap_detection_on_unreachable = models.SmallIntegerField()
    low_flap_threshold = models.FloatField()
    high_flap_threshold = models.FloatField()
    process_performance_data = models.SmallIntegerField()
    freshness_checks_enabled = models.SmallIntegerField()
    freshness_threshold = models.SmallIntegerField()
    passive_checks_enabled = models.SmallIntegerField()
    event_handler_enabled = models.SmallIntegerField()
    active_checks_enabled = models.SmallIntegerField()
    retain_status_information = models.SmallIntegerField()
    retain_nonstatus_information = models.SmallIntegerField()
    notifications_enabled = models.SmallIntegerField()
    obsess_over_host = models.SmallIntegerField()
    failure_prediction_enabled = models.SmallIntegerField()
    notes = models.CharField(max_length=255)
    notes_url = models.CharField(max_length=255)
    action_url = models.CharField(max_length=255)
    icon_image = models.CharField(max_length=255)
    icon_image_alt = models.CharField(max_length=255)
    vrml_image = models.CharField(max_length=255)
    statusmap_image = models.CharField(max_length=255)
    have_2d_coords = models.SmallIntegerField()
    x_2d = models.SmallIntegerField()
    y_2d = models.SmallIntegerField()
    have_3d_coords = models.SmallIntegerField()
    x_3d = models.FloatField()
    y_3d = models.FloatField()
    z_3d = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nagios_hosts'


class NagiosHoststatus(models.Model):
    hoststatus_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    host_object_id = models.IntegerField(unique=True)
    status_update_time = models.DateTimeField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()
    perfdata = models.TextField()
    current_state = models.SmallIntegerField()
    has_been_checked = models.SmallIntegerField()
    should_be_scheduled = models.SmallIntegerField()
    current_check_attempt = models.SmallIntegerField()
    max_check_attempts = models.SmallIntegerField()
    last_check = models.DateTimeField()
    next_check = models.DateTimeField()
    check_type = models.SmallIntegerField()
    last_state_change = models.DateTimeField()
    last_hard_state_change = models.DateTimeField()
    last_hard_state = models.SmallIntegerField()
    last_time_up = models.DateTimeField()
    last_time_down = models.DateTimeField()
    last_time_unreachable = models.DateTimeField()
    state_type = models.SmallIntegerField()
    last_notification = models.DateTimeField()
    next_notification = models.DateTimeField()
    no_more_notifications = models.SmallIntegerField()
    notifications_enabled = models.SmallIntegerField()
    problem_has_been_acknowledged = models.SmallIntegerField()
    acknowledgement_type = models.SmallIntegerField()
    current_notification_number = models.SmallIntegerField()
    passive_checks_enabled = models.SmallIntegerField()
    active_checks_enabled = models.SmallIntegerField()
    event_handler_enabled = models.SmallIntegerField()
    flap_detection_enabled = models.SmallIntegerField()
    is_flapping = models.SmallIntegerField()
    percent_state_change = models.FloatField()
    latency = models.FloatField()
    execution_time = models.FloatField()
    scheduled_downtime_depth = models.SmallIntegerField()
    failure_prediction_enabled = models.SmallIntegerField()
    process_performance_data = models.SmallIntegerField()
    obsess_over_host = models.SmallIntegerField()
    modified_host_attributes = models.IntegerField()
    event_handler = models.CharField(max_length=255)
    check_command = models.CharField(max_length=255)
    normal_check_interval = models.FloatField()
    retry_check_interval = models.FloatField()
    check_timeperiod_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_hoststatus'


class NagiosInstances(models.Model):
    instance_id = models.SmallIntegerField(primary_key=True)
    instance_name = models.CharField(max_length=64)
    instance_description = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'nagios_instances'


class NagiosLogentries(models.Model):
    logentry_id = models.AutoField(primary_key=True)
    instance_id = models.IntegerField()
    logentry_time = models.DateTimeField()
    entry_time = models.DateTimeField()
    entry_time_usec = models.IntegerField()
    logentry_type = models.IntegerField()
    logentry_data = models.CharField(max_length=255)
    realtime_data = models.SmallIntegerField()
    inferred_data_extracted = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_logentries'


class NagiosNotifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    notification_type = models.SmallIntegerField()
    notification_reason = models.SmallIntegerField()
    object_id = models.IntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    state = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()
    escalated = models.SmallIntegerField()
    contacts_notified = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_notifications'


class NagiosObjects(models.Model):
    object_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    objecttype_id = models.SmallIntegerField()
    name1 = models.CharField(max_length=128)
    name2 = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_objects'


class NagiosProcessevents(models.Model):
    processevent_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    event_type = models.SmallIntegerField()
    event_time = models.DateTimeField()
    event_time_usec = models.IntegerField()
    process_id = models.IntegerField()
    program_name = models.CharField(max_length=16)
    program_version = models.CharField(max_length=20)
    program_date = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'nagios_processevents'


class NagiosProgramstatus(models.Model):
    programstatus_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField(unique=True)
    status_update_time = models.DateTimeField()
    program_start_time = models.DateTimeField()
    program_end_time = models.DateTimeField()
    is_currently_running = models.SmallIntegerField()
    process_id = models.IntegerField()
    daemon_mode = models.SmallIntegerField()
    last_command_check = models.DateTimeField()
    last_log_rotation = models.DateTimeField()
    notifications_enabled = models.SmallIntegerField()
    active_service_checks_enabled = models.SmallIntegerField()
    passive_service_checks_enabled = models.SmallIntegerField()
    active_host_checks_enabled = models.SmallIntegerField()
    passive_host_checks_enabled = models.SmallIntegerField()
    event_handlers_enabled = models.SmallIntegerField()
    flap_detection_enabled = models.SmallIntegerField()
    failure_prediction_enabled = models.SmallIntegerField()
    process_performance_data = models.SmallIntegerField()
    obsess_over_hosts = models.SmallIntegerField()
    obsess_over_services = models.SmallIntegerField()
    modified_host_attributes = models.IntegerField()
    modified_service_attributes = models.IntegerField()
    global_host_event_handler = models.CharField(max_length=255)
    global_service_event_handler = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_programstatus'


class NagiosRuntimevariables(models.Model):
    runtimevariable_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    varname = models.CharField(max_length=64)
    varvalue = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_runtimevariables'


class NagiosScheduleddowntime(models.Model):
    scheduleddowntime_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    downtime_type = models.SmallIntegerField()
    object_id = models.IntegerField()
    entry_time = models.DateTimeField()
    author_name = models.CharField(max_length=64)
    comment_data = models.CharField(max_length=255)
    internal_downtime_id = models.IntegerField()
    triggered_by_id = models.IntegerField()
    is_fixed = models.SmallIntegerField()
    duration = models.SmallIntegerField()
    scheduled_start_time = models.DateTimeField()
    scheduled_end_time = models.DateTimeField()
    was_started = models.SmallIntegerField()
    actual_start_time = models.DateTimeField()
    actual_start_time_usec = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_scheduleddowntime'


class NagiosServiceContactgroups(models.Model):
    service_contactgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    service_id = models.IntegerField()
    contactgroup_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_service_contactgroups'


class NagiosServiceContacts(models.Model):
    service_contact_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    service_id = models.IntegerField()
    contact_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_service_contacts'


class NagiosServicechecks(models.Model):
    servicecheck_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    service_object_id = models.IntegerField()
    check_type = models.SmallIntegerField()
    current_check_attempt = models.SmallIntegerField()
    max_check_attempts = models.SmallIntegerField()
    state = models.SmallIntegerField()
    state_type = models.SmallIntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    command_object_id = models.IntegerField()
    command_args = models.CharField(max_length=255)
    command_line = models.CharField(max_length=255)
    timeout = models.SmallIntegerField()
    early_timeout = models.SmallIntegerField()
    execution_time = models.FloatField()
    latency = models.FloatField()
    return_code = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()
    perfdata = models.TextField()

    class Meta:
        managed = False
        db_table = 'nagios_servicechecks'


class NagiosServicedependencies(models.Model):
    servicedependency_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    service_object_id = models.IntegerField()
    dependent_service_object_id = models.IntegerField()
    dependency_type = models.SmallIntegerField()
    inherits_parent = models.SmallIntegerField()
    timeperiod_object_id = models.IntegerField()
    fail_on_ok = models.SmallIntegerField()
    fail_on_warning = models.SmallIntegerField()
    fail_on_unknown = models.SmallIntegerField()
    fail_on_critical = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_servicedependencies'


class NagiosServiceescalationContactgroups(models.Model):
    serviceescalation_contactgroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    serviceescalation_id = models.IntegerField()
    contactgroup_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_serviceescalation_contactgroups'


class NagiosServiceescalationContacts(models.Model):
    serviceescalation_contact_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    serviceescalation_id = models.IntegerField()
    contact_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_serviceescalation_contacts'


class NagiosServiceescalations(models.Model):
    serviceescalation_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    service_object_id = models.IntegerField()
    timeperiod_object_id = models.IntegerField()
    first_notification = models.SmallIntegerField()
    last_notification = models.SmallIntegerField()
    notification_interval = models.FloatField()
    escalate_on_recovery = models.SmallIntegerField()
    escalate_on_warning = models.SmallIntegerField()
    escalate_on_unknown = models.SmallIntegerField()
    escalate_on_critical = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_serviceescalations'


class NagiosServicegroupMembers(models.Model):
    servicegroup_member_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    servicegroup_id = models.IntegerField()
    service_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_servicegroup_members'


class NagiosServicegroups(models.Model):
    servicegroup_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    servicegroup_object_id = models.IntegerField()
    alias = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_servicegroups'


class NagiosServices(models.Model):
    service_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    host_object_id = models.IntegerField()
    service_object_id = models.IntegerField()
    display_name = models.CharField(max_length=64)
    check_command_object_id = models.IntegerField()
    check_command_args = models.CharField(max_length=255)
    eventhandler_command_object_id = models.IntegerField()
    eventhandler_command_args = models.CharField(max_length=255)
    notification_timeperiod_object_id = models.IntegerField()
    check_timeperiod_object_id = models.IntegerField()
    failure_prediction_options = models.CharField(max_length=64)
    check_interval = models.FloatField()
    retry_interval = models.FloatField()
    max_check_attempts = models.SmallIntegerField()
    first_notification_delay = models.FloatField()
    notification_interval = models.FloatField()
    notify_on_warning = models.SmallIntegerField()
    notify_on_unknown = models.SmallIntegerField()
    notify_on_critical = models.SmallIntegerField()
    notify_on_recovery = models.SmallIntegerField()
    notify_on_flapping = models.SmallIntegerField()
    notify_on_downtime = models.SmallIntegerField()
    stalk_on_ok = models.SmallIntegerField()
    stalk_on_warning = models.SmallIntegerField()
    stalk_on_unknown = models.SmallIntegerField()
    stalk_on_critical = models.SmallIntegerField()
    is_volatile = models.SmallIntegerField()
    flap_detection_enabled = models.SmallIntegerField()
    flap_detection_on_ok = models.SmallIntegerField()
    flap_detection_on_warning = models.SmallIntegerField()
    flap_detection_on_unknown = models.SmallIntegerField()
    flap_detection_on_critical = models.SmallIntegerField()
    low_flap_threshold = models.FloatField()
    high_flap_threshold = models.FloatField()
    process_performance_data = models.SmallIntegerField()
    freshness_checks_enabled = models.SmallIntegerField()
    freshness_threshold = models.SmallIntegerField()
    passive_checks_enabled = models.SmallIntegerField()
    event_handler_enabled = models.SmallIntegerField()
    active_checks_enabled = models.SmallIntegerField()
    retain_status_information = models.SmallIntegerField()
    retain_nonstatus_information = models.SmallIntegerField()
    notifications_enabled = models.SmallIntegerField()
    obsess_over_service = models.SmallIntegerField()
    failure_prediction_enabled = models.SmallIntegerField()
    notes = models.CharField(max_length=255)
    notes_url = models.CharField(max_length=255)
    action_url = models.CharField(max_length=255)
    icon_image = models.CharField(max_length=255)
    icon_image_alt = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_services'


class NagiosServicestatus(models.Model):
    servicestatus_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    service_object_id = models.IntegerField(unique=True)
    status_update_time = models.DateTimeField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()
    perfdata = models.TextField()
    current_state = models.SmallIntegerField()
    has_been_checked = models.SmallIntegerField()
    should_be_scheduled = models.SmallIntegerField()
    current_check_attempt = models.SmallIntegerField()
    max_check_attempts = models.SmallIntegerField()
    last_check = models.DateTimeField()
    next_check = models.DateTimeField()
    check_type = models.SmallIntegerField()
    last_state_change = models.DateTimeField()
    last_hard_state_change = models.DateTimeField()
    last_hard_state = models.SmallIntegerField()
    last_time_ok = models.DateTimeField()
    last_time_warning = models.DateTimeField()
    last_time_unknown = models.DateTimeField()
    last_time_critical = models.DateTimeField()
    state_type = models.SmallIntegerField()
    last_notification = models.DateTimeField()
    next_notification = models.DateTimeField()
    no_more_notifications = models.SmallIntegerField()
    notifications_enabled = models.SmallIntegerField()
    problem_has_been_acknowledged = models.SmallIntegerField()
    acknowledgement_type = models.SmallIntegerField()
    current_notification_number = models.SmallIntegerField()
    passive_checks_enabled = models.SmallIntegerField()
    active_checks_enabled = models.SmallIntegerField()
    event_handler_enabled = models.SmallIntegerField()
    flap_detection_enabled = models.SmallIntegerField()
    is_flapping = models.SmallIntegerField()
    percent_state_change = models.FloatField()
    latency = models.FloatField()
    execution_time = models.FloatField()
    scheduled_downtime_depth = models.SmallIntegerField()
    failure_prediction_enabled = models.SmallIntegerField()
    process_performance_data = models.SmallIntegerField()
    obsess_over_service = models.SmallIntegerField()
    modified_service_attributes = models.IntegerField()
    event_handler = models.CharField(max_length=255)
    check_command = models.CharField(max_length=255)
    normal_check_interval = models.FloatField()
    retry_check_interval = models.FloatField()
    check_timeperiod_object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_servicestatus'


class NagiosStatehistory(models.Model):
    statehistory_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    state_time = models.DateTimeField()
    state_time_usec = models.IntegerField()
    object_id = models.IntegerField()
    state_change = models.SmallIntegerField()
    state = models.SmallIntegerField()
    state_type = models.SmallIntegerField()
    current_check_attempt = models.SmallIntegerField()
    max_check_attempts = models.SmallIntegerField()
    last_state = models.SmallIntegerField()
    last_hard_state = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()

    class Meta:
        managed = False
        db_table = 'nagios_statehistory'


class NagiosSystemcommands(models.Model):
    systemcommand_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    start_time = models.DateTimeField()
    start_time_usec = models.IntegerField()
    end_time = models.DateTimeField()
    end_time_usec = models.IntegerField()
    command_line = models.CharField(max_length=255)
    timeout = models.SmallIntegerField()
    early_timeout = models.SmallIntegerField()
    execution_time = models.FloatField()
    return_code = models.SmallIntegerField()
    output = models.CharField(max_length=255)
    long_output = models.TextField()

    class Meta:
        managed = False
        db_table = 'nagios_systemcommands'


class NagiosTimedeventqueue(models.Model):
    timedeventqueue_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    event_type = models.SmallIntegerField()
    queued_time = models.DateTimeField()
    queued_time_usec = models.IntegerField()
    scheduled_time = models.DateTimeField()
    recurring_event = models.SmallIntegerField()
    object_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_timedeventqueue'


class NagiosTimedevents(models.Model):
    timedevent_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    event_type = models.SmallIntegerField()
    queued_time = models.DateTimeField()
    queued_time_usec = models.IntegerField()
    event_time = models.DateTimeField()
    event_time_usec = models.IntegerField()
    scheduled_time = models.DateTimeField()
    recurring_event = models.SmallIntegerField()
    object_id = models.IntegerField()
    deletion_time = models.DateTimeField()
    deletion_time_usec = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_timedevents'


class NagiosTimeperiodTimeranges(models.Model):
    timeperiod_timerange_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    timeperiod_id = models.IntegerField()
    day = models.SmallIntegerField()
    start_sec = models.IntegerField()
    end_sec = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nagios_timeperiod_timeranges'


class NagiosTimeperiods(models.Model):
    timeperiod_id = models.AutoField(primary_key=True)
    instance_id = models.SmallIntegerField()
    config_type = models.SmallIntegerField()
    timeperiod_object_id = models.IntegerField()
    alias = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'nagios_timeperiods'
