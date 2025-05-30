import requests

class RiseCRMError(Exception):
    """Exceção customizada para erros da API do Rise CRM."""
    pass

class RiseCRMClient:
    """
    Cliente para consumir a API REST do RISE CRM.
    Todos os métodos autenticam usando o header 'authtoken'.
    """
    def __init__(self, base_url: str, authtoken: str):
        self.base_url = base_url.rstrip('/')
        self.authtoken = authtoken
        self.session = requests.Session()
        self.session.headers.update({"authtoken": self.authtoken})

    # -------------------- LEADS --------------------
    def add_lead(self, **kwargs):
        """Adiciona um novo lead. POST /index.php/api/leads"""
        raise NotImplementedError

    def delete_lead(self, lead_id):
        """Deleta um lead. DELETE /index.php/api/leads/:id"""
        raise NotImplementedError

    def get_lead(self, lead_id):
        """Obtém informações de um lead. GET /index.php/api/leads/:leadid"""
        raise NotImplementedError

    def search_leads(self, query):
        """Busca leads. GET /index.php/api/leads/search/:keysearch"""
        raise NotImplementedError

    def update_lead(self, lead_id, **kwargs):
        """Atualiza um lead. PUT /index.php/api/leads/:id"""
        raise NotImplementedError

    def list_leads(self):
        """Lista todos os leads. GET /index.php/api/leads"""
        raise NotImplementedError

    # -------------------- PROJECTS --------------------
    def add_project(self, **kwargs):
        """Adiciona um novo projeto. POST /index.php/api/projects"""
        raise NotImplementedError

    def delete_project(self, project_id):
        """Deleta um projeto. DELETE /index.php/api/projects/:id"""
        raise NotImplementedError

    def list_projects(self):
        """Lista todos os projetos. GET /index.php/api/projects"""
        raise NotImplementedError

    def search_projects(self, query):
        """Busca projetos. GET /index.php/api/projects/search/:keysearch"""
        raise NotImplementedError

    def update_project(self, project_id, **kwargs):
        """Atualiza um projeto. PUT /index.php/api/projects/:id"""
        raise NotImplementedError

    # -------------------- TICKETS --------------------
    def add_ticket(self, **kwargs):
        """Adiciona um novo ticket. POST /index.php/api/tickets"""
        raise NotImplementedError

    def delete_ticket(self, ticket_id):
        """Deleta um ticket. DELETE /index.php/api/tickets/:id"""
        raise NotImplementedError

    def get_ticket(self, ticket_id):
        """Obtém informações de um ticket. GET /index.php/api/tickets/:ticketid"""
        raise NotImplementedError

    def search_tickets(self, query):
        """Busca tickets. GET /index.php/api/tickets/search/:keysearch"""
        raise NotImplementedError

    def update_ticket(self, ticket_id, **kwargs):
        """Atualiza um ticket. PUT /index.php/api/tickets/:id"""
        raise NotImplementedError

    # -------------------- INVOICES --------------------
    def add_invoice(self, **kwargs):
        """Adiciona uma nova invoice. POST /index.php/api/invoices"""
        raise NotImplementedError

    def delete_invoice(self, invoice_id):
        """Deleta uma invoice. DELETE /index.php/api/invoices/:id"""
        raise NotImplementedError

    def get_invoice(self, invoice_id):
        """Obtém informações de uma invoice. GET /index.php/api/invoices/:invoiceid"""
        raise NotImplementedError

    def search_invoices(self, query):
        """Busca invoices. GET /index.php/api/invoices/search/:keysearch"""
        raise NotImplementedError

    def update_invoice(self, invoice_id, **kwargs):
        """Atualiza uma invoice. PUT /index.php/api/invoices/:id"""
        raise NotImplementedError

    # -------------------- CLIENTS --------------------
    def add_client(self, **kwargs):
        """Adiciona um novo cliente. POST /index.php/api/clients"""
        raise NotImplementedError

    def delete_client(self, client_id):
        """Deleta um cliente. DELETE /index.php/api/clients/:id"""
        raise NotImplementedError

    def get_client(self, client_id):
        """Obtém informações de um cliente. GET /index.php/api/clients/:clientid"""
        raise NotImplementedError

    def search_clients(self, query):
        """Busca clientes. GET /index.php/api/getClientsSearch/search/:keysearch"""
        raise NotImplementedError

    # -------------------- MISCELLANEOUS --------------------
    def get_client_groups(self):
        """Lista grupos de clientes. GET /index.php/api/client_groups"""
        raise NotImplementedError

    def get_contacts_by_client(self, client_id):
        """Lista contatos por client ID. GET /index.php/api/contact_by_clientid/:clientid"""
        raise NotImplementedError

    def get_invoice_labels(self):
        """Lista labels de invoice. GET /index.php/api/invoice_labels"""
        raise NotImplementedError

    def get_invoice_taxes(self):
        """Lista taxes de invoice. GET /index.php/api/invoice_tax"""
        raise NotImplementedError

    def get_project_labels(self):
        """Lista labels de projeto. GET /index.php/api/project_labels"""
        raise NotImplementedError

    def get_project_members(self):
        """Lista membros de projeto. GET /index.php/api/getProjectMembers"""
        raise NotImplementedError

    def get_staff_owner(self):
        """Lista staff/owners. GET /index.php/api/staff_owner"""
        raise NotImplementedError

    def get_ticket_labels(self):
        """Lista labels de ticket. GET /index.php/api/ticket_labels"""
        raise NotImplementedError

    def get_ticket_types(self):
        """Lista tipos de ticket. GET /index.php/api/ticket_type"""
        raise NotImplementedError 