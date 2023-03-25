NEW = 'NEW'
IN_DISCUSSION = 'IN_DISCUSSION'
REJECTED = 'REJECTED'
IN_PROGRESS = 'IN_PROGRESS'
FULFILLED = 'FULFILLED'
TICKET_STATUS_ENUM = [NEW, IN_DISCUSSION, REJECTED, IN_PROGRESS, FULFILLED]

class TicketWorkflow:
    NEW = [IN_DISCUSSION]
    IN_DISCUSSION = [REJECTED, IN_PROGRESS]
    IN_PROGRESS = [FULFILLED]
    