import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
from tkinter.font import Font
from typing import Tuple, Optional, Dict
import io
from odf.opendocument import load


class ModernButton(tk.Canvas):
    """
    Classe personalizada para criar botões modernos com efeitos visuais.
    Herda de tk.Canvas para permitir desenho personalizado.
    """

    def __init__(self, master=None, width=400, height=50, corner_radius=12,
                 bg_color="#FFFFFF", fg_color="#014A78", hover_color="#0168A8",
                 click_color="#013A5E", text_color="white", text="Button",
                 font=("Segoe UI", 11, "bold"), command=None, **kwargs):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bg=bg_color, **kwargs)

        # Configurações do botão
        self.command = command  # Função a ser executada quando clicado
        self.corner_radius = corner_radius  # Raio dos cantos arredondados
        self.fg_color = fg_color  # Cor normal
        self.hover_color = hover_color  # Cor quando mouse está sobre
        self.click_color = click_color  # Cor quando clicado
        self.text = text  # Texto do botão
        self.text_color = text_color  # Cor do texto
        self.font = font  # Fonte do texto
        self.width = width  # Largura
        self.height = height  # Altura
        self.bg_color = bg_color  # Cor de fundo
        self.is_pressed = False  # Estado do botão

        self.draw_button(self.fg_color)  # Desenha o botão inicialmente

        # Vincula eventos do mouse
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def draw_button(self, color):
        """Desenha o botão com cantos arredondados e texto"""
        self.delete("all")  # Limpa o canvas
        radius = self.corner_radius

        # Desenha os 4 cantos arredondados
        self.create_arc(0, 0, 2 * radius, 2 * radius, start=90, extent=90,
                        fill=color, outline=color)
        self.create_arc(self.width - 2 * radius, 0, self.width, 2 * radius, start=0, extent=90,
                        fill=color, outline=color)
        self.create_arc(0, self.height - 2 * radius, 2 * radius, self.height, start=180, extent=90,
                        fill=color, outline=color)
        self.create_arc(self.width - 2 * radius, self.height - 2 * radius, self.width, self.height,
                        start=270, extent=90, fill=color, outline=color)

        # Desenha os retângulos centrais
        self.create_rectangle(radius, 0, self.width - radius, self.height,
                              fill=color, outline=color)
        self.create_rectangle(0, radius, self.width, self.height - radius,
                              fill=color, outline=color)

        # Adiciona o texto
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                         fill=self.text_color, font=self.font)

    def on_enter(self, event):
        """Evento quando o mouse entra no botão"""
        if not self.is_pressed:
            self.draw_button(self.hover_color)

    def on_leave(self, event):
        """Evento quando o mouse sai do botão"""
        if not self.is_pressed:
            self.draw_button(self.fg_color)

    def on_press(self, event):
        """Evento quando o botão é pressionado"""
        self.is_pressed = True
        self.draw_button(self.click_color)

    def on_release(self, event):
        """Evento quando o botão é liberado"""
        self.is_pressed = False
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        if widget == self:
            self.draw_button(self.hover_color)
            if self.command:
                self.command()  # Executa a função associada
        else:
            self.draw_button(self.fg_color)


class ComparadorPlanilhasApp:
    """
    Classe principal da aplicação que implementa o comparador de planilhas.
    """

    def __init__(self, root):
        self.root = root
        self.planilha_alterdata = None  # Armazena a planilha ALTERDATA
        self.planilha_santri = None  # Armazena a planilha SANTRI
        self.configurar_janela()
        self.criar_widgets()

        # Configuração flexível das colunas esperadas
        self.colunas_esperadas = {
            'ALTERDATA': {
                'colunas_originais': ['Número', 'Nome Forn/Cliente', 'Valor Contábil', ],
                'mapeamento': {
                    'Número': 'nota_fiscal',
                    'Nome Forn/Cliente': 'fornecedor',
                    'Valor Contábil': 'valor',

                }
            },
            'SANTRI': {
                'colunas_originais': ['Número', 'Cadastro', 'Valor contábil'],
                'mapeamento': {
                    'Número': 'nota_fiscal',
                    'Cadastro': 'fornecedor',
                    'Valor contábil': 'valor'
                }
            }
        }

    def configurar_janela(self):
        """Configura a janela principal da aplicação"""
        self.root.title("Comparador de Planilhas 📊")
        self.root.configure(bg="#F5F7FA")
        self.root.state("zoomed")  # Maximiza a janela
        self.root.resizable(False, False)  # Tamanho fixo

        # Configura o estilo dos widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background="#F5F7FA")
        self.style.configure('TNotebook.Tab',
                             background="#D1D9E6",
                             foreground="#053760",
                             padding=[15, 5],
                             font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab',
                       background=[('selected', '#FFFFFF')],
                       expand=[('selected', [1, 1, 1, 0])])

    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#E8ECF4", padx=0, pady=0)
        self.frame_principal.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)

        # Frame interno para borda visual
        self.frame_interno = tk.Frame(self.frame_principal, bg="#FFFFFF", bd=0,
                                      highlightthickness=0, relief='ridge')
        self.frame_interno.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)

        # Frame de conteúdo principal
        self.frame_conteudo = tk.Frame(self.frame_interno, bg="#FFFFFF")
        self.frame_conteudo.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Título da aplicação
        self.titulo_frame = tk.Frame(self.frame_conteudo, bg="#FFFFFF")
        self.titulo_frame.pack(pady=(20, 30))

        self.titulo = tk.Label(
            self.titulo_frame,
            text="Comparador de Planilhas📊",
            font=("Segoe UI", 28, "bold"),
            bg="#FFFFFF",
            fg="#053760"
        )
        self.titulo.pack()

        # Frame para status das planilhas
        self.frame_status = tk.Frame(self.frame_conteudo, bg="#FFFFFF")
        self.frame_status.pack(pady=10)

        # Labels para mostrar status das planilhas
        self.label_alterdata = tk.Label(
            self.frame_status,
            text="● Nenhuma planilha ALTERDATA selecionada",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#7F8FA4",
            padx=10
        )
        self.label_alterdata.pack(anchor="w", pady=5)

        self.label_santri = tk.Label(
            self.frame_status,
            text="● Nenhuma planilha SANTRI ADM selecionada",
            font=("Segoe UI", 12),
            bg="#FFFFFF",
            fg="#7F8FA4",
            padx=10
        )
        self.label_santri.pack(anchor="w", pady=5)

        # Frame para os botões
        self.frame_botoes = tk.Frame(self.frame_conteudo, bg="#FFFFFF")
        self.frame_botoes.pack(pady=20)

        # Botão para carregar planilha ALTERDATA
        self.btn_alterdata = ModernButton(
            self.frame_botoes,
            width=400,
            height=50,
            corner_radius=12,
            fg_color="#014A78",
            hover_color="#0168A8",
            click_color="#013A5E",
            text="📂 ADICIONAR PLANILHA ALTERDATA",
            command=self.carregar_alterdata
        )
        self.btn_alterdata.pack(pady=10)

        # Botão para carregar planilha SANTRI
        self.btn_santri = ModernButton(
            self.frame_botoes,
            width=400,
            height=50,
            corner_radius=12,
            fg_color="#014A78",
            hover_color="#0168A8",
            click_color="#013A5E",
            text="📂 ADICIONAR PLANILHA SANTRI ADM",
            command=self.carregar_santri
        )
        self.btn_santri.pack(pady=10)

        # Botão para comparar planilhas
        self.btn_comparar = ModernButton(
            self.frame_botoes,
            width=400,
            height=50,
            corner_radius=12,
            fg_color="#28A745",
            hover_color="#34CE57",
            click_color="#1E7E34",
            text="🔍 COMPARAR PLANILHAS",
            command=self.comparar_planilhas
        )
        self.btn_comparar.pack(pady=20)

        # Botão para sair
        self.btn_sair = ModernButton(
            self.frame_botoes,
            width=400,
            height=50,
            corner_radius=12,
            fg_color="#C70909",
            hover_color="#E82C2C",
            click_color="#A00606",
            text="🚪 Sair do Sistema",
            command=self.sair
        )
        self.btn_sair.pack(pady=10)

        # Frame para mostrar resultados
        self.frame_resultados = tk.Frame(self.frame_conteudo, bg="#FFFFFF")
        self.frame_resultados.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Inicialmente desabilita o botão de comparar
        self.btn_comparar.config(state=tk.DISABLED)

    def verificar_arquivos_carregados(self):
        """Habilita o botão de comparar se ambas planilhas estiverem carregadas"""
        if self.planilha_alterdata is not None and self.planilha_santri is not None:
            self.btn_comparar.config(state=tk.NORMAL)
            self.btn_comparar.draw_button("#34CE57")
        else:
            self.btn_comparar.config(state=tk.DISABLED)
            self.btn_comparar.draw_button("#28A745")

    def detectar_formato_arquivo(self, caminho_arquivo: str) -> str:
        """Detecta o formato do arquivo baseado na extensão e conteúdo"""
        extensao = os.path.splitext(caminho_arquivo)[1].lower()

        if extensao in ('.xlsx', '.xls'):
            return 'excel'
        elif extensao == '.csv':
            return 'csv'
        elif extensao == '.ods':
            return 'ods'
        else:
            # Tenta detectar pelo conteúdo
            with open(caminho_arquivo, 'rb') as f:
                inicio = f.read(8).decode('ascii', errors='ignore')
                if 'PK' in inicio:
                    return 'excel'
                elif '<?xml' in inicio:
                    return 'ods'
                else:
                    return 'csv'

    def ler_arquivo(self, caminho: str, tipo: str) -> Optional[pd.DataFrame]:
        """
        Lê um arquivo de planilha e verifica se contém as colunas necessárias.

        Args:
            caminho: Caminho do arquivo
            tipo: Tipo da planilha ('ALTERDATA' ou 'SANTRI')

        Returns:
            DataFrame com os dados ou None em caso de erro
        """
        try:
            formato = self.detectar_formato_arquivo(caminho)

            # Lê o arquivo conforme o formato detectado
            if formato == 'excel':
                try:
                    skiprows = 0 if tipo == 'ALTERDATA' else 4
                    df = pd.read_excel(caminho, engine='openpyxl', skiprows=skiprows)
                except:
                    df = pd.read_excel(caminho, engine='xlrd', skiprows=skiprows)
            elif formato == 'csv':
                # Tenta diferentes codificações para CSV
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                for encoding in encodings:
                    try:
                        df = pd.read_csv(caminho, encoding=encoding, delimiter=None, engine='python')
                        break
                    except UnicodeDecodeError:
                        continue
            elif formato == 'ods':
                df = pd.read_excel(caminho, engine='odf')
            else:
                raise ValueError(f"Formato não suportado: {formato}")

            # Verifica se o tipo é ALTERDATA ou SANTRI
            tipo_planilha = tipo.split()[0].upper()
            config = self.colunas_esperadas.get(tipo_planilha, {})

            if not config:
                raise ValueError(f"Tipo de planilha desconhecido: {tipo}")

            # Verifica colunas obrigatórias
            colunas_obrigatorias = config['colunas_originais']
            colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]

            if colunas_faltantes:
                raise ValueError(
                    f"Colunas faltando na planilha {tipo}:\n"
                    f"{', '.join(colunas_faltantes)}\n\n"
                    f"Colunas encontradas: {', '.join(df.columns)}"
                )

            return df

        except Exception as e:
            # Tratamento de erros específicos
            if "No engine" in str(e):
                erro_msg = "Falha ao ler Excel. Verifique:\n1. Arquivo não corrompido\n2. Bibliotecas instaladas"
            elif "UnicodeDecodeError" in str(e):
                erro_msg = "Problema de codificação. Salve como UTF-8 ou Excel."
            else:
                erro_msg = str(e)

            messagebox.showerror("Erro", f"Erro ao ler {tipo}:\n{erro_msg}")
            return None

    def carregar_alterdata(self):
        """Abre diálogo para selecionar e carregar planilha ALTERDATA"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha ALTERDATA",
            filetypes=[
                ("Planilhas Excel", "*.xlsx *.xls"),
                ("Arquivos CSV", "*.csv"),
                ("Planilhas ODS", "*.ods"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if arquivo:
            self.planilha_alterdata = self.ler_arquivo(arquivo, "ALTERDATA")
            if self.planilha_alterdata is not None:
                nome = os.path.basename(arquivo)
                self.label_alterdata.config(text=f"✓ Planilha ALTERDATA: {nome}", fg="#28A745")
                self.verificar_arquivos_carregados()
            else:
                self.label_alterdata.config(text=f"✗ Erro ao carregar ALTERDATA", fg="#C70909")

    def carregar_santri(self):
        """Abre diálogo para selecionar e carregar planilha SANTRI"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha SANTRI ADM",
            filetypes=[
                ("Planilhas Excel", "*.xlsx *.xls"),
                ("Arquivos CSV", "*.csv"),
                ("Planilhas ODS", "*.ods"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if arquivo:
            self.planilha_santri = self.ler_arquivo(arquivo, "SANTRI ADM")
            if self.planilha_santri is not None:
                nome = os.path.basename(arquivo)
                self.label_santri.config(text=f"✓ Planilha SANTRI ADM: {nome}", fg="#28A745")
                self.verificar_arquivos_carregados()
            else:
                self.label_santri.config(text=f"✗ Erro ao carregar SANTRI", fg="#C70909")

    def comparar_planilhas(self):
        """Compara as planilhas carregadas e mostra as diferenças"""
        try:
            if self.planilha_alterdata is None or self.planilha_santri is None:
                messagebox.showerror("Erro", "Carregue ambas as planilhas antes de comparar")
                return

            # Padroniza os nomes das colunas
            alterdata = self.planilha_alterdata.rename(
                columns=self.colunas_esperadas['ALTERDATA']['mapeamento']
            )

            santri = self.planilha_santri.rename(
                columns=self.colunas_esperadas['SANTRI']['mapeamento']
            )

            # Padroniza os dados
            alterdata['nota_fiscal'] = alterdata['nota_fiscal'].astype(str).str.strip()
            santri['nota_fiscal'] = santri['nota_fiscal'].astype(str).str.strip()
            alterdata['fornecedor'] = alterdata['fornecedor'].astype(str).str.strip()
            santri['fornecedor'] = santri['fornecedor'].astype(str).str.strip()

            # Converte valores para float
            alterdata['valor'] = pd.to_numeric(alterdata['valor'], errors='coerce')
            santri['valor'] = pd.to_numeric(santri['valor'], errors='coerce')

            # Faz o merge das planilhas
            merged = pd.merge(
                alterdata, santri,
                on=['nota_fiscal', 'fornecedor', 'valor'],
                how='outer',
                indicator=True
            )

            # Separa os resultados
            apenas_alterdata = merged[merged['_merge'] == 'left_only']
            apenas_santri = merged[merged['_merge'] == 'right_only']

            self.mostrar_resultados(apenas_alterdata, apenas_santri)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comparar:\n{str(e)}")

    def mostrar_resultados(self, apenas_alterdata: pd.DataFrame, apenas_santri: pd.DataFrame):
        """Mostra os resultados da comparação em abas"""
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        notebook = ttk.Notebook(self.frame_resultados)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Cria aba para notas faltantes na SANTRI
        frame_alterdata = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(frame_alterdata, text=f"[35mFaltantes na Alterdata Selecionado({len(apenas_alterdata)})".upper())

        # Cria aba para notas faltantes na ALTERDATA
        frame_santri = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(frame_santri, text=f"Faltantes na Santri Selecionado  ({len(apenas_santri)})".upper())

        # Preenche as tabelas
        self.preencher_tabela(frame_alterdata, apenas_alterdata)
        self.preencher_tabela(frame_santri, apenas_santri)

    def preencher_tabela(self, frame, dados):
        """Preenche uma tabela com os dados fornecidos"""
        if len(dados) == 0:
            # Mostra mensagem se não houver diferenças
            tk.Label(
                frame,
                text="✔ Todas as notas estão presentes",
                font=("Segoe UI", 12),
                bg="#FFFFFF",
                fg="#28A745"
            ).pack(expand=True)
            return

        # Configura o estilo da tabela
        style = ttk.Style()
        style.configure("Treeview",
                        font=('Segoe UI', 15),
                        rowheight=25,
                        background="#FFFFFF",
                        fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading",
                        font=('Segoe UI', 15, 'bold'),
                        background="#E8ECF4",
                        foreground="#053760")
        style.map("Treeview",
                  background=[('selected', "#B1F6B5")],
                  foreground=[('selected', '#053760')])

        tree_frame = tk.Frame(frame, bg="#FFFFFF")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cria a Treeview
        columns = ['nota_fiscal', 'fornecedor', 'valor']
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Configura cabeçalhos
        tree.heading('nota_fiscal', text='Nota Fiscal')
        tree.heading('fornecedor', text='Fornecedor')
        tree.heading('valor', text='Valor (R$)')

        # Configura largura das colunas
        tree.column('nota_fiscal', width=150, anchor=tk.CENTER)
        tree.column('fornecedor', width=300, anchor=tk.CENTER)
        tree.column('valor', width=150, anchor=tk.CENTER)

        # Adiciona scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Preenche a tabela com os dados
        for _, row in dados.iterrows():
            try:
                valor_formatado = f"R$ {float(row['valor']):,.2f}" if pd.notna(
                    row['valor']) else " R$ 0,00"
                tree.insert('', tk.END, values=(
                    row['nota_fiscal'],
                    row['fornecedor'],
                    valor_formatado
                ))
            except Exception as e:
                print(f"Erro ao adicionar linha: {e}")

    def sair(self):
        """Fecha a aplicação após confirmação"""
        if messagebox.askyesno("Sair", "Deseja realmente fechar o programa?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ComparadorPlanilhasApp(root)
    root.mainloop()