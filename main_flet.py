import flet as ft
from database.db import Database
from controllers.material_controller import MaterialController
from controllers.obra_controller import ObraController
from controllers.compra_controller import CompraController
from controllers.atividade_controller import AtividadeController
from controllers.medicao_controller import MedicaoController
from controllers.despesa_controller import DespesaController
from models.evm_model import EVMModel

def main(page: ft.Page):
    # Configuração da página
    page.title = "Gestão de Obras - Moderno"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 1200
    page.window.height = 800
    
    # Database e Controllers
    db = Database()
    material_ctrl = MaterialController(db)
    obra_ctrl = ObraController(db)
    compra_ctrl = CompraController(db, material_ctrl, obra_ctrl)
    atividade_ctrl = AtividadeController(db)
    medicao_ctrl = MedicaoController(db)
    despesa_ctrl = DespesaController(db)
    evm_model = EVMModel(db)
    
    # Índice da página atual
    current_page = ft.Ref[int]()
    current_page.current = 0
    
    # ========== VIEWS ==========
    
    def criar_view_materiais():
        """View de Materiais com design moderno"""
        
        # Tabela de materiais
        materiais_data = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Unidade", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.Colors.GREY_200),
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
        )
        
        def carregar_materiais():
            """Carrega materiais na tabela"""
            materiais = material_ctrl.listar()
            materiais_data.rows.clear()
            
            for m in materiais:
                materiais_data.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(m.get("id", "")))),
                            ft.DataCell(ft.Text(str(m.get("codigo", "")))),
                            ft.DataCell(ft.Text(str(m.get("descricao", "")))),
                            ft.DataCell(ft.Text(str(m.get("unidade", "")))),
                        ]
                    )
                )
            page.update()
        
        def abrir_dialog_novo_material(e):
            """Dialog para adicionar novo material"""
            codigo_field = ft.TextField(label="Código", width=300)
            descricao_field = ft.TextField(label="Descrição", width=300)
            unidade_field = ft.TextField(label="Unidade", width=300)
            
            def salvar_material(e):
                if codigo_field.value and descricao_field.value and unidade_field.value:
                    material_ctrl.criar_material(
                        codigo_field.value,
                        descricao_field.value,
                        unidade_field.value
                    )
                    dialog.open = False
                    carregar_materiais()
                    page.show_snack_bar(
                        ft.SnackBar(ft.Text("Material criado com sucesso!"), bgcolor=ft.Colors.GREEN)
                    )
                    page.update()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Novo Material"),
                content=ft.Column([
                    codigo_field,
                    descricao_field,
                    unidade_field,
                ], tight=True, spacing=20),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog()),
                    ft.ElevatedButton("Salvar", on_click=salvar_material),
                ],
            )
            
            def fechar_dialog():
                dialog.open = False
                page.update()
            
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
        
        # Carregar materiais inicialmente
        carregar_materiais()
        
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("Materiais", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.ElevatedButton(
                                "Novo Material",
                                icon=ft.Icons.ADD,
                                on_click=abrir_dialog_novo_material,
                            ),
                            ft.ElevatedButton(
                                "Atualizar",
                                icon=ft.Icons.REFRESH,
                                on_click=lambda e: carregar_materiais(),
                            ),
                        ], spacing=10),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                ),
                # Tabela
                ft.Container(
                    content=ft.Column([
                        materiais_data,
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20,
                    expand=True,
                ),
            ]),
            expand=True,
        )
    
    def criar_view_obras():
        return ft.Container(
            content=ft.Text("Obras - Em construção", size=30),
            alignment=ft.alignment.center,
            expand=True,
        )
    
    def criar_view_compras():
        return ft.Container(
            content=ft.Text("Compras - Em construção", size=30),
            alignment=ft.alignment.center,
            expand=True,
        )
    
    def criar_view_boas_vindas():
        """Tela de boas-vindas inicial"""
        return ft.Container(
            content=ft.Column([
                # Logo da empresa
                ft.Image(
                    src="assets/logo.png",
                    width=400,
                    height=250,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Container(height=20),
                ft.Text(
                    "Sistema de Gestão de Obras",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Container(height=10),
                ft.Text(
                    "Gerencie suas obras, materiais, compras e muito mais",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
            ),
            alignment=ft.alignment.center,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_50, ft.Colors.WHITE],
            ),
        )
    
    # ========== NAVEGAÇÃO ==========
    
    content_area = ft.Container(expand=True)
    
    def mudar_pagina(index):
        """Muda a página exibida"""
        current_page.current = index
        
        if index == 0:
            content_area.content = criar_view_boas_vindas()
        elif index == 1:
            content_area.content = criar_view_obras()
        elif index == 2:
            content_area.content = criar_view_materiais()
        elif index == 3:
            content_area.content = criar_view_compras()
        
        page.update()
    
    # Menu lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CONSTRUCTION,
                selected_icon=ft.Icons.CONSTRUCTION,
                label="Obras",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.Icons.INVENTORY_2,
                label="Materiais",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SHOPPING_CART_OUTLINED,
                selected_icon=ft.Icons.SHOPPING_CART,
                label="Compras",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ATTACH_MONEY,
                selected_icon=ft.Icons.ATTACH_MONEY,
                label="Financeiro",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ANALYTICS_OUTLINED,
                selected_icon=ft.Icons.ANALYTICS,
                label="EVM",
            ),
        ],
        on_change=lambda e: mudar_pagina(e.control.selected_index),
        bgcolor=ft.Colors.BLUE_GREY_50,
    )
    
    # Layout principal
    mudar_pagina(0)  # Inicia na tela de boas-vindas
    
    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1),
            content_area,
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.app(target=main)
