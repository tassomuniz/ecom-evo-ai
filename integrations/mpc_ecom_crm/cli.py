import argparse
import sys
from mpc_ecom_crm.client import RiseCRMClient, RiseCRMError

def main():
    parser = argparse.ArgumentParser(description="CLI para testar o RiseCRMClient")
    parser.add_argument('--base_url', required=True, help='URL base da API do RISE CRM')
    parser.add_argument('--authtoken', required=True, help='Token de autenticação')

    subparsers = parser.add_subparsers(dest='command')

    # Exemplo: adicionar lead
    add_lead_parser = subparsers.add_parser('add-lead', help='Adicionar um novo lead')
    add_lead_parser.add_argument('--company_name', required=True)
    add_lead_parser.add_argument('--owner_id', required=True)
    # Adicione outros campos conforme necessário

    # Exemplo: listar projetos
    list_projects_parser = subparsers.add_parser('list-projects', help='Listar todos os projetos')

    # Exemplo: buscar leads
    search_leads_parser = subparsers.add_parser('search-leads', help='Buscar leads')
    search_leads_parser.add_argument('--query', required=True)

    args = parser.parse_args()

    client = RiseCRMClient(base_url=args.base_url, authtoken=args.authtoken)

    try:
        if args.command == 'add-lead':
            print('Adicionando lead...')
            # Exemplo de uso (ajuste os campos conforme implementação real)
            result = client.add_lead(company_name=args.company_name, owner_id=args.owner_id)
            print(result)
        elif args.command == 'list-projects':
            print('Listando projetos...')
            result = client.list_projects()
            print(result)
        elif args.command == 'search-leads':
            print(f'Buscando leads: {args.query}')
            result = client.search_leads(args.query)
            print(result)
        else:
            parser.print_help()
    except RiseCRMError as e:
        print(f'Erro na API: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main() 