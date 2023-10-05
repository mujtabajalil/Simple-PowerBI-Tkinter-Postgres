
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import pandas as pd
# import the ttk
from tkinter import ttk
import psycopg2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sqlalchemy import create_engine


class CreateWelcomeFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.widget = 1300
        self.height = 610
        self.highlightbackground = "black"
        self.highlightthickness = 1
        self.DEBUG_MODE = container.DEBUG_MODE
        self.DEBUG_MODE = True
        self.config(bg="white")
        self.propagate(False)
        selected_csvs : int = 0
        selected_csvs_path : str = ""
    
        

        if self.DEBUG_MODE == True:
            self.configure(highlightbackground="black")
            self.configure(highlightthickness=1)

        # make 2 frames
        self.left_frame = tk.Frame(self, width=300, height=580)
        self.left_frame.grid(row=0, column=1, padx=0, pady=0)
        self.left_frame.grid_propagate(False)
        self.left_frame.config(bg="white")
        
        # add padding to left frame
        self.left_frame.grid(padx=30)
        self.left_frame.grid(pady=20)
        
        if self.DEBUG_MODE == True:
            self.left_frame.configure(highlightbackground="black")
            self.left_frame.configure(highlightthickness=1)
            
            
        self.right_frame = tk.Frame(self, width=900, height=580)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)
        self.right_frame.grid_propagate(False)
        self.right_frame.config(bg="white")
        
        # add padding to right frame
        self.right_frame.grid(padx=30)
        self.right_frame.grid(pady=20)
        
        if self.DEBUG_MODE == True:
            self.right_frame.configure(highlightbackground="black")
            self.right_frame.configure(highlightthickness=1)
            
            
        self.add_buttons(self.left_frame)
        
    def add_buttons(self, parent_frame):
        # add buttons to left frame with name open CSV
        self.open_csv_button = tk.Button(parent_frame, text="Open CSV", width=20, height=2)
        self.open_csv_button.grid(row=1, column=0, padx=50, pady=30)
        self.open_csv_button.config(borderwidth=2)
        #call show_csvs function when button is clicked
        self.open_csv_button.config(command=lambda: self.show_csvs(self.right_frame)) 
        
        
        # add buttons to left frame with name open CSV
        self.connect_to_postgres = tk.Button(parent_frame, text="Postgres Conn", width=20, height=2)
        self.connect_to_postgres.grid(row=0, column=0, padx=50, pady=30)
        self.connect_to_postgres.config(borderwidth=2)
        # call functoin conn_to_db
        self.connect_to_postgres.config(command=lambda: self.conn_to_db(self.right_frame))
        
        
        # visualization button
        self.visualizations_button = tk.Button(parent_frame, text="Visualizations", width=20, height=2)
        self.visualizations_button.grid(row=2, column=0, padx=50, pady=30)
        self.visualizations_button.config(borderwidth=2)
        # Call the show_visualizations function when button is clicked
        self.visualizations_button.config(command=lambda: self.show_visualizations())
        
    def show_visualizations(self):
        for child in self.right_frame.winfo_children():
            child.grid_forget()
        # show box plot of each column of df1 in right_frame
        
        # # tak the first column of df1 and plot it
        # # create a figure
        # fig = Figure(figsize=(5,5), dpi=100)
        # # add a subplot
        # ax = fig.add_subplot(111)
        # # plot the data
        
        # firstCol = self.df1.iloc[:,0]
        # ax.boxplot(firstCol)
        # # ax.boxplot([1,2,3,4,5,6,7,8,9,10])
        
        # # create a canvas
        # canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=0, column=0, padx=50, pady=30)
        
        # create 2 frames top and bottom
        self.right_top_frame = tk.Frame(self.right_frame, width=900, height=50)
        self.right_top_frame.grid(row=0, column=0, padx=0, pady=0)
        self.right_top_frame.grid_propagate(False)
        
        if self.DEBUG_MODE == True:
            self.right_top_frame.configure(highlightbackground="black")
            self.right_top_frame.configure(highlightthickness=1)
            
        # add a button named shoe Mean/Mode/Median
        self.mean_mode_median_button = tk.Button(self.right_top_frame, text="Mean/Mode/Median", width=20, height=2)
        self.mean_mode_median_button.grid(row=0, column=0, padx=3, pady=3)
        
        # call show_mean_mode_median function
        self.mean_mode_median_button.config(command=lambda: self.show_mean_mode_median())
        
        
        # create a button show chart
        self.show_chart_button = tk.Button(self.right_top_frame, text="Show Chart", width=20, height=2)
        self.show_chart_button.grid(row=0, column=1, padx=3, pady=3)
        
        # call show_chart function
        self.show_chart_button.config(command=lambda: self.show_chart())
            
        self.right_bottom_frame = tk.Frame(self.right_frame, width=900, height=600)
        self.right_bottom_frame.grid(row=1, column=0, padx=0, pady=0)
        self.right_bottom_frame.grid_propagate(False)
        
        if self.DEBUG_MODE == True:
            self.right_bottom_frame.configure(highlightbackground="black")
            self.right_bottom_frame.configure(highlightthickness=1)
    
    def show_chart(self):
        
        # hide all the child of right_bottom_frame
        for child in self.right_bottom_frame.winfo_children():
            child.grid_forget()
        
        import pandas as pd
        import matplotlib.pyplot as plt

        allowed_eids = ['C18A', 'C18F', 'C188']
        filtered_df = self.df2[self.df2['EID'].isin(allowed_eids)]
        filtered_df1 = self.df1[self.df1['id'].isin(filtered_df['id'])]
        
        merged_df = pd.merge(filtered_df, filtered_df1, on='id', how='inner')
        
        # Filter the DataFrame based on the three EIDs
        filtered_df = merged_df[merged_df['EID'].isin(['C18A', 'C18F', 'C188'])]

        # Clean column names by stripping spaces
        filtered_df.columns = filtered_df.columns.str.strip()

        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(5, 5))

        # Group the data by 'EID' and calculate unique counts for each column
        grouped_data = filtered_df.groupby('EID')[['Site', 'Freq.', 'Block', 'Serv Label1', 'Serv Label2', 'Serv Label3', 'Serv Label4']].nunique()

        # Transpose the grouped data for plotting
        transposed_data = grouped_data.T

        # Plot the grouped bar chart
        transposed_data.plot(kind='bar', ax=ax)
        ax.set_ylabel('Count')
        ax.set_title('Counts of Attributes for EIDs C18A, C18F, C188')
        # plt.xticks(rotation=0)
        # plt.tight_layout()
        # plt.show()
        
        # resize the figure
        fig.set_size_inches(5, 5)
        
        # convert plt to image
        fig.savefig("chart.png")
        
        # show image in tkinter
        self.img = ImageTk.PhotoImage(Image.open("chart.png"))
        
        self.img_label = tk.Label(self.right_bottom_frame, image=self.img)
        self.img_label.grid(row=0, column=0, padx=5, pady=5)
        
        
       
                
    def show_mean_mode_median(self):
        for child in self.right_bottom_frame.winfo_children():
            child.grid_forget()
            
            
        allowed_eids = ['C18A', 'C18F', 'C188']
        filtered_df = self.df2[self.df2['EID'].isin(allowed_eids)]
        filtered_df1 = self.df1[self.df1['id'].isin(filtered_df['id'])]
        
        merged_df = pd.merge(filtered_df, filtered_df1, on='id', how='inner')
        
        
        from statistics import mode

        # Filter based on conditions
        filtered_df = merged_df[
            (merged_df['EID'].isin(['C18A', 'C18F', 'C188'])) &
            (merged_df['Site Height'] > 75) &
            (pd.to_datetime(merged_df['Date'], format='%d/%m/%Y').dt.year >= 2001)
        ]

        # Create an empty dictionary to store the results for each EID
        results = {}

        # Loop through each unique EID and calculate mean, mode, and median
        for eid in filtered_df['EID'].unique():
            eid_data = filtered_df[filtered_df['EID'] == eid]
            mean_erp = eid_data['In-Use ERP Total'].mean()
            mode_erp = mode(eid_data['In-Use ERP Total'])
            median_erp = eid_data['In-Use ERP Total'].median()
            results[eid] = {'Mean': mean_erp, 'Mode': mode_erp, 'Median': median_erp}

        # Create a DataFrame from the results dictionary
        result_df = pd.DataFrame(results)
        # add a column in start with column name desc and data as mean, mode, median
        result_df['desc'] = ['Mean', 'Mode', 'Median']
        
        # create a treeview to show the data
        self.treeview3 = ttk.Treeview(self.right_bottom_frame, columns=list(result_df.columns), show="headings", height=20)
        self.treeview3.grid(row=0, column=0, pady=5, ipadx=5, ipady=5)
        
        # now display each column in treeview
        for column in list(result_df.columns):
            self.treeview3.heading(column, text=column)
            
        # add data to treeview
        for index, row in result_df.iterrows():
            self.treeview3.insert("", "end", values=list(row))
        
        
            
        
            
        
        
        
        
        
        
    def conn_to_db(self, parent_frame):
        for child in parent_frame.winfo_children():
            child.grid_forget()
            
        # add a field in the right frame to enter the database name
        self.db_name_label = tk.Label(parent_frame, text="Database Name", width=20, height=2)
        self.db_name_label.grid(row=0, column=0, padx=50, pady=30)
        self.db_name_label.config(borderwidth=2)
        
        self.db_name_entry = tk.Entry(parent_frame, width=20, borderwidth=2)
        self.db_name_entry.grid(row=0, column=1, padx=50, pady=30)
        
        # get username
        self.username_label = tk.Label(parent_frame, text="Username", width=20, height=2)
        self.username_label.grid(row=1, column=0, padx=50, pady=30)
        self.username_label.config(borderwidth=2)
        
        self.username_entry = tk.Entry(parent_frame, width=20, borderwidth=2)
        self.username_entry.grid(row=1, column=1, padx=50, pady=30)
        
        # get password
        self.password_label = tk.Label(parent_frame, text="Password", width=20, height=2)
        self.password_label.grid(row=2, column=0, padx=50, pady=30)
        self.password_label.config(borderwidth=2)
        
        self.password_entry = tk.Entry(parent_frame, width=20, borderwidth=2)
        self.password_entry.grid(row=2, column=1, padx=50, pady=30)
        
        
        # add a button to connect to database
        self.connect_to_db_button = tk.Button(parent_frame, text="Connect", width=20, height=2)
        self.connect_to_db_button.grid(row=3, column=0, padx=50, pady=30)
        self.connect_to_db_button.config(borderwidth=2)
        
        # call function to connect to database
        
        self.connect_to_db_button.config(command=lambda: self.connect_to_db(self.db_name_entry.get().strip(), self.username_entry.get().strip(), self.password_entry.get().strip()))
        
        # add a red label on roght side to show connection status
        self.connection_status_label = tk.Label(parent_frame, text="Not Connected", width=20, height=2)
        self.connection_status_label.grid(row=3, column=1, padx=50, pady=30)
        self.connection_status_label.config(borderwidth=2)
        self.connection_status_label.config(bg="red")
        
    
        
        
    def connect_to_db(self, db_name, username, password):
        # connect to database
        self.conn = psycopg2.connect(database=db_name, user=username, password=password, host="localhost", port=5432)
        # check if conn successful
        if self.conn:
            self.connection_status_label.config(bg="green")
            # change label to connected
            self.connection_status_label.config(text="Connected")
            
            
        # get all the tables in the database
        self.cur = self.conn.cursor()
        # SQL statement to create the table
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS public.ante (
                id SERIAL PRIMARY KEY,
                NGR VARCHAR,
                "Site Height" INTEGER,
                "In-Use Ae Ht" INTEGER,
                "In-Use ERP Total" NUMERIC,
                Lat NUMERIC,
                Long NUMERIC
            );
        '''
        
        # run the sql statement
        self.cur.execute(create_table_sql)
        
        # commit the changes
        self.conn.commit()
        
        # close the connection
        self.conn.close()
        self.cur.close()
        
        
        create_table_sql_2 = """
            CREATE TABLE IF NOT EXISTS public.param (
                id SERIAL PRIMARY KEY,
                Date DATE,
                "EID" VARCHAR(255),
                "Site" VARCHAR(255),
                "Freq" VARCHAR(255),
                "Block" VARCHAR(255),
                "Serv Label1" VARCHAR(255),
                "Serv Label2" VARCHAR(255),
                "Serv Label3" VARCHAR(255),
                "Serv Label4" VARCHAR(255),
                "Serv Label10" VARCHAR(255)
            );
        
        """
        self.conn = psycopg2.connect(database=db_name, user=username, password=password, host="localhost", port=5432)
        self.cur = self.conn.cursor()
        self.cur.execute(create_table_sql_2)
        self.conn.commit()
        self.conn.close()
        self.cur.close()
        
        
        
        
        
        
    def show_csvs(self, parent_frame):
        
        # hide all childs in right_frame
        for child in parent_frame.winfo_children():
            child.grid_forget()
        # ask user to select multiple csvs
        self.csvs = filedialog.askopenfilenames(initialdir="/jill0", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # check length of csvs
        if len(self.csvs) == 2:
            self.p1 = self.csvs[0]
            self.p2 = self.csvs[1]    
            
            print (self.p1.split("/")[-1])
            
            # check the name of first csv
            if self.p1.split("/")[-1] == "Ante.csv":
                # read csvs
                self.df1 = pd.read_csv(self.p1, encoding='latin-1')
                self.df2 = pd.read_csv(self.p2, encoding='latin-1')
                
            else:
                self.df1 = pd.read_csv(self.p2, encoding='latin-1')
                self.df2 = pd.read_csv(self.p1, encoding='latin-1')
            
            
        
        
    
        
        # create 3 frames top, middle, bottom
        self.top_frame = tk.Frame(parent_frame, width=800, height=50)
        self.top_frame.grid(row=0, column=0, padx=5, pady=5)
        self.top_frame.grid_propagate(False)
        
        if self.DEBUG_MODE == True:
            self.top_frame.configure(highlightbackground="black")
            self.top_frame.configure(highlightthickness=1)
            
        # add 2 buttons to top frame named csv1 and csv2
        self.csv1_button = tk.Button(self.top_frame, text="CSV1", width=20, height=2)
        self.csv1_button.grid(row=0, column=0, padx=50, pady=4)
        self.csv1_button.config(borderwidth=2)
        # call show_csv_1 function when button is clicked
        self.csv1_button.config(command=lambda: self.show_csv_1())
        
              
      
        
        self.csv2_button = tk.Button(self.top_frame, text="CSV2", width=20, height=2)
        self.csv2_button.grid(row=0, column=1, padx=50, pady=4)
        self.csv2_button.config(borderwidth=2)
        # call show_csv_2
        self.csv2_button.config(command=lambda: self.show_csv_2())
        
            
        self.middle_frame = tk.Frame(parent_frame, width=800, height=450)
        self.middle_frame.grid(row=1, column=0, padx=5, pady=5)
        self.middle_frame.grid_propagate(False)
        
        if self.DEBUG_MODE == True:
            self.middle_frame.configure(highlightbackground="black")
            self.middle_frame.configure(highlightthickness=1)
            
        self.bottom_frame = tk.Frame(parent_frame, width=800, height=50)
        self.bottom_frame.grid(row=2, column=0, padx=5, pady=5)
        self.bottom_frame.grid_propagate(False)
        
        if self.DEBUG_MODE == True:
            self.bottom_frame.configure(highlightbackground="black")
            self.bottom_frame.configure(highlightthickness=1)
            
        #add a button at the button at the bpttom called clean data and call clean_data function
        self.clean_data_button = tk.Button(self.bottom_frame, text="Clean Data", width=20, height=2)
        self.clean_data_button.grid(row=0, column=0, padx=50, pady=4)
        self.clean_data_button.config(borderwidth=2)
        self.clean_data_button.config(command=lambda: self.clean_data())
        
    def clean_data(self):
        # get the name of the selected csv
        name = self.selected_csvs_path.split("/")[-1]
        if name == "Ante.csv":
            self.clean_ante_data()
        elif name == "Param.csv":
            self.clean_param_data()
        
    def add_to_postgres(self,df, table_name, schema):
        """
        Add a dataframe to a postgres table
        """
        
        your_password = "5csCpqp5vUSs8fN"
        dbname = self.db_name_entry.get().strip()
        user = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        connection_params = {
            'host': 'localhost',
            'port': 5432,
            'dbname': dbname,
            'user': user,
            'password': password,
        }
        
        # self.db_name_entry.get().strip(), self.username_entry.get().strip(), self.password_entry.get().strip()

        # Establish a connection using psycopg2
        conn = psycopg2.connect(**connection_params)

        try:
            # Create an SQLAlchemy engine using the established connection
            engine = create_engine('postgresql://', creator=lambda: conn)
            
            # Use the engine to insert the DataFrame into the table
            df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)

        except Exception as e:
            print("Error:", e)
        
    
    def clean_ante_data(self):
        print("Here")
        threshold = len(self.df1) - 50  # Calculate the threshold

        # Drop columns with non-NaN values below the threshold
        cleaned_df = self.df1.dropna(axis=1, thresh=threshold)

        drop_col = 'Longitude/Latitude'
        cleaned_df.drop(drop_col, axis=1, inplace=True)

        cleaned_df['In-Use ERP Total'] = cleaned_df['In-Use ERP Total'].str.replace('"', '').str.replace(',', '').astype(float)
        cleaned_df['Lat'] = cleaned_df['Lat'].astype(float)
        cleaned_df['Long'] = cleaned_df['Long'].astype(float)

        # Update the self.df2 attribute with the cleaned DataFrame
        self.df1 = cleaned_df
        
        # remove all data in treeview2
        self.treeview1.delete(*self.treeview1.get_children())
        # remove all headings in treeview1
        self.treeview1["columns"] = []
        
        # add the new columns to treeview1
        self.treeview1["columns"] = list(self.df1.columns)
        
        cols = list(self.df1.columns)
        
        for column in cols:
            self.treeview1.heading(column, text=column)
        
        
        # print(self.df1.columns)
        
        # # add the new columns to treeview2
        # self.treeview1["columns"] = list(self.df1.columns)
        # add the new data
        for i in range(len(self.df1)):
            self.treeview1.insert("", "end", values=list(self.df1.iloc[i]))
            
            
        self.add_to_postgres(self.df1, "ante", "public")
            
    
        
    
   
        
        
        
    def clean_param_data(self):
        threshold = len(self.df2) - 50  # Calculate the threshold

        # Drop columns with non-NaN values below the threshold
        cleaned_df = self.df2.dropna(axis=1, thresh=threshold)

        columns_to_delete = [
            'SId 1 (Hex)', 'SId 3 (Hex)', 'SId 6 (Hex)', 'Serv Label7 ',
            'SId 7 (Hex)', 'SId 2 (Hex)', 'SId 4 (Hex)', 'Serv Label5 ',
            'SId 5 (Hex)', 'Serv Label6 ', 'Ensemble', 'Licence',
            'Ensemble Area', 'Transmitter Area', 'TII Main Id (Hex)',
            'TII Sub Id (Hex)'
        ]

        # Delete the specified columns
        cleaned_df = cleaned_df.drop(columns=columns_to_delete)

        # Convert "Date" column to date format
        cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'], format='%d/%m/%Y')

        # Update the self.df1 attribute with the cleaned DataFrame
        self.df2 = cleaned_df
        
        self.treeview2.delete(*self.treeview2.get_children())
        # remove all headings in treeview1
        self.treeview2["columns"] = []
        
        # add the new columns to treeview1
        self.treeview2["columns"] = list(self.df2.columns)
        
        cols = list(self.df2.columns)
        
        for column in cols:
            self.treeview2.heading(column, text=column)
        
        
        # print(self.df1.columns)
        
        # # add the new columns to treeview2
        # self.treeview1["columns"] = list(self.df1.columns)
        # add the new data
        for i in range(len(self.df2)):
            self.treeview2.insert("", "end", values=list(self.df2.iloc[i]))

       
            
    def show_csv_2(self):
        self.selected_csvs = 2
        self.selected_csvs_path  = self.p2
        
        # hide all in middle frame
        for widget in self.middle_frame.winfo_children():
            widget.destroy()
        
        
        cols = self.df2.columns.tolist()
        # print (cols)
        
        # create a small treeview with 2 columns
        self.treeview2 = ttk.Treeview(self.middle_frame, columns=cols, show="headings", height=20)
        self.treeview2.grid(row=0, column=0, pady=5, ipadx=5, ipady=5)
        
        
        # add scrollbar to treeview
        self.scrollbar1 = ttk.Scrollbar(self.middle_frame, orient="vertical", command=self.treeview2.yview)
        self.scrollbar1.grid(row=1, column=1, sticky="ns")
        self.treeview2.configure(yscrollcommand=self.scrollbar1.set)
        
        # add a horizontal scrollbar
        self.scrollbar2 = ttk.Scrollbar(self.middle_frame, orient="horizontal", command=self.treeview2.xview)
        self.scrollbar2.grid(row=1, column=0, sticky="ew")
        self.treeview2.configure(xscrollcommand=self.scrollbar2.set)
        
         # add columns to treeview
        for column in cols:
            self.treeview2.heading(column, text=column)
            
        # add data to treeview
        for index, row in self.df2.iterrows():
            self.treeview2.insert("", "end", values=list(row))
            
            
    
    
    def show_csv_1(self):
        self.selected_csvs = 1
        self.selected_csvs_path = self.p1
        
        # hide all in middle frame
        for widget in self.middle_frame.winfo_children():
            widget.destroy()
        
        columns1 = self.df1.columns.tolist()
        print (columns1)
        
        
        # create a small treeview with 2 columns
        self.treeview1 = ttk.Treeview(self.middle_frame, columns=columns1, show="headings", height=20)
        self.treeview1.grid(row=0, column=0, pady=5, ipadx=5, ipady=5)
        
                
       
            
        # add scrollbar to treeview
        self.scrollbar1 = ttk.Scrollbar(self.middle_frame, orient="vertical", command=self.treeview1.yview)
        self.scrollbar1.grid(row=1, column=1, sticky="ns")
        self.treeview1.configure(yscrollcommand=self.scrollbar1.set)
        
        # add a horizontal scrollbar
        self.scrollbar2 = ttk.Scrollbar(self.middle_frame, orient="horizontal", command=self.treeview1.xview)
        self.scrollbar2.grid(row=2, column=0, sticky="ew")
        self.treeview1.configure(xscrollcommand=self.scrollbar2.set)
        
         # add columns to treeview
        for column in columns1:
            self.treeview1.heading(column, text=column)
            
        # add data to treeview
        for index, row in self.df1.iterrows():
            self.treeview1.insert("", "end", values=list(row))
        
        
        
        
        
        
        
        
    def show(self):
        self.grid(row=1, column=0, padx=0, pady=0)
    
    def hide(self):
        self.grid_forget()
        