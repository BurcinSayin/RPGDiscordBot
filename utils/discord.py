# creating enumerations using class
import enum


class InteractionType(enum.Enum):
    # * A ping.
    PING = 1
    # * A command invocation.
    APPLICATION_COMMAND = 2
    # * Usage of a message's component.
    MESSAGE_COMPONENT = 3
    # * An interaction sent when an application command option is filled out.
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    # * An interaction sent when a modal is submitted.
    APPLICATION_MODAL_SUBMIT = 5


class InteractionResponseType(enum.Enum):
    # * Acknowledge a `PING`.
    PONG = 1
    # *Respond with a message, showing the user's input.
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    # * Acknowledge a command without sending a message, showing the user's input. Requires follow-up.
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    # * Acknowledge an interaction and edit the original message that contains the component later; the user does not see a loading state.
    DEFERRED_UPDATE_MESSAGE = 6
    # * Edit the message the component was attached to.
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    APPLICATION_MODAL = 9


class InteractionOptionType(enum.Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4    # Any     integer    between - 2 ^ 53 and 2 ^ 53
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7    # Includes    all    channel    types + categories
    ROLE = 8
    MENTIONABLE = 9    # Includes    users and roles
    NUMBER = 10    # Any    double    between - 2 ^ 53 and 2 ^ 53
    ATTACHMENT = 11    # attachment    object
