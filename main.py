import flet as ft
import sqlite3
class Todo:
    def __init__(self,page:ft.Page):
        self.page = page
        self.page.scroll="adaptive"
        self.page.bgcolor = ft.colors.WHITE
        self.page.window_width=400
        self.page.window_height=450
        self.page.window_resizable = False
        self.page.window_always_on_top = True
        self.page.title = 'TodoApp'
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name,status)')
        self.result = self.db_execute('SELECT * FROM  tasks')

        self.task=""
        self.view='all'
        self.main_page()
    
    def db_execute(self,query,params=[]):
         with sqlite3.connect('database.db')as con:
              cur = con.cursor()
              cur.execute(query,params)
              con.commit()
              return cur.fetchall()
              
    def checked(self,e):
         is_checked = e.control.value
         label=e.control.label
         if is_checked:
              self.db_execute('UPDATE tasks SET status = "completo" WHERE name =?' , params=[label] )
         else:
              self.db_execute('UPDATE tasks SET status = "icompleto" WHERE name =?' , params=[label] )

         if self.view=='all':
              self.result = self.db_execute("SELECT * FROM tasks")  
         else:
              self.result = self.db_execute("SELECT * FROM tasks WHERE status = ?",params=[self.view])  
              self.update_task_list()       

    def tasks_container(self):

        return ft.Container(
            height=self.page.height *0.8,
            content=ft.Column(
                
                controls=[
                         
                         ft.Checkbox(label=res[0], 
                         on_change = self.checked ,   
                         value = True if res[1]=='completo' else False)
                    
                         for res in self.result if res
                   
                ]
                         
            )
        )
    def set_value(self,e):
         self.task = e.control.value
    #funcao inserir dados
    def add(self,e,input_task):
        name = self.task
        status = "incompleto"
        if name:
             self.db_execute(query = 'INSERT INTO tasks VALUES(?,?)',params=[name,status])
             input_task.value = ""
             self.result = self.db_execute('SELECT * FROM  tasks')
             self.update_task_list()
    
    def update_task_list(self):
         tasks =self.tasks_container()
         self.page.controls.pop()
         self.page.add(tasks)
         self.page.update()
    def tabs_changed(self,e):
         if e.control.selected_index==0:
              self.result = self.db_execute('SELECT * FROM tasks')
              self.view = 'all'
         elif e.control.selected_index==1:
              self.result = self.db_execute('SELECT * FROM tasks WHERE status ="incompleto"')  
              self.view = 'incompleto' 
         elif e.control.selected_index==2:
              self.result = self.db_execute('SELECT * FROM tasks WHERE status = "completo"') 
              self.view = 'completo'
         self.update_task_list()   

    def main_page(self):
           input_task = ft.TextField(hint_text="Dgite a Tarefa",expand=True,
                                     on_change=self.set_value)

           input_bar = ft.Row(
                controls=[
                     input_task,
                     ft.FloatingActionButton(icon=ft.icons.ADD,
                                             on_click=lambda e:self.add(e,input_task))
                ]
           )
           tab = ft.Tabs(
               selected_index=0,
               on_change=self.tabs_changed,
               tabs=[
                   ft.Tab(text='Tarefas'),
                   ft.Tab(text='Em Andamento'),
                   ft.Tab(text='Realizadas')                                 
                 
                   
               ]
           )
           tasks = self.tasks_container()
           self.page.add(
                
                input_bar,
                tab,
                tasks

           )
ft.app(target=Todo)