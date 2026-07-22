from tkinter import *
from tkinter import messagebox

from backend import PasswordManagerBE

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class PasswordManagerGUI:
    def __init__(self, master):
        self.be = PasswordManagerBE()
        self.master = master
        master.title("Password Manager")
        master.config(padx=50, pady=50)

        # ------------------------------------------------------------
        # الشعار (اختياري - لا يوقف البرنامج إن لم يوجد logo.png)
        # ------------------------------------------------------------
        self.canvas = Canvas(height=200, width=200, highlightthickness=0)
        try:
            self.logo = PhotoImage(file='logo.png')
            self.canvas.create_image(100, 100, image=self.logo)
        except TclError:
            self.canvas.create_text(100, 100, text="🔐", font=("Arial", 60))
        self.canvas.grid(row=0, column=1)

        # ------------------------------------------------------------
        # التسميات
        # ------------------------------------------------------------
        Label(text='Website:').grid(row=1, column=0, sticky='W')
        Label(text='Email:').grid(row=2, column=0, sticky='W')
        Label(text='Password:').grid(row=3, column=0, sticky='W')

        # ------------------------------------------------------------
        # المتغيرات وحقول الإدخال
        # ------------------------------------------------------------
        self.website_var = StringVar()
        self.email_var = StringVar()
        self.password_var = StringVar()

        self.website_entry = Entry(width=39, textvariable=self.website_var)
        self.website_entry.grid(row=1, column=1, columnspan=3, sticky='NSEW')
        self.website_entry.focus()
        # يسمح بالبحث بالضغط على Enter داخل حقل الموقع
        self.website_entry.bind('<Return>', lambda event: self.search_password())

        self.email_entry = Entry(width=39, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=1, columnspan=3, sticky='NSEW')

        # كلمة المرور تظهر كنجوم افتراضياً، مع زر لإظهارها
        self.password_entry = Entry(width=24, textvariable=self.password_var, show='*')
        self.password_entry.grid(row=3, column=1, columnspan=2, sticky='NSEW')

        # ------------------------------------------------------------
        # الأزرار
        # ------------------------------------------------------------
        Button(text='Generate', command=self.generate_password).grid(
            row=3, column=3, sticky='NSEW')

        self.show_password_button = Button(text='👁', width=3, command=self.toggle_password_visibility)
        self.show_password_button.grid(row=3, column=4, sticky='NSEW')

        Button(text='Add', command=self.save_data).grid(
            row=4, column=1, sticky='NSEW')
        Button(text='Clear', command=self.clear).grid(
            row=4, column=2, sticky='NSEW')
        Button(text='Search', command=self.search_password).grid(
            row=4, column=3, sticky='NSEW')
        Button(text='Delete', command=self.delete_password, fg='red').grid(
            row=4, column=4, sticky='NSEW')

    # ------------------------------------------------------------------
    # الأحداث
    # ------------------------------------------------------------------
    def generate_password(self):
        password = self.be.generate_password()
        self.password_var.set(password)

        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            messagebox.showinfo(title='تم التوليد', message='تم توليد كلمة المرور ونسخها للحافظة')
        else:
            messagebox.showinfo(title='تم التوليد', message='تم توليد كلمة المرور')

    def toggle_password_visibility(self):
        current = self.password_entry.cget('show')
        self.password_entry.config(show='' if current == '*' else '*')

    def save_data(self):
        website = self.website_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        if not website or not email or not password:
            messagebox.showinfo(title='تحذير', message='الرجاء التأكد من عدم ترك أي حقل فارغاً!')
            return

        if self.be.website_exists(website):
            overwrite = messagebox.askyesno(
                title='الموقع موجود مسبقاً',
                message=f'يوجد بيانات محفوظة مسبقاً لـ "{website}".\nهل تريد استبدالها بالبيانات الجديدة؟'
            )
            if not overwrite:
                return

        self.be.save_data(website, email, password)
        self.clear()
        messagebox.showinfo(title='نجاح', message='تم الحفظ بنجاح!')

    def search_password(self):
        website = self.website_var.get().strip()
        if not website:
            messagebox.showinfo(title='تحذير', message='الرجاء إدخال اسم الموقع أولاً')
            return

        result = self.be.search_password(website)
        if result is None:
            messagebox.showinfo(title='غير موجود', message='لم نجد كلمة مرور محفوظة لهذا الموقع')
        else:
            _, _, email, password = result
            self.email_var.set(email)
            self.password_var.set(password)
            # يعرض كلمة المرور مؤقتاً عند البحث حتى يقدر المستخدم يقرأها/ينسخها
            self.password_entry.config(show='')

    def delete_password(self):
        website = self.website_var.get().strip()
        if not website:
            messagebox.showinfo(title='تحذير', message='الرجاء إدخال اسم الموقع أولاً')
            return

        confirm = messagebox.askyesno(
            title='تأكيد الحذف',
            message=f'هل أنت متأكد من حذف بيانات "{website}"؟'
        )
        if not confirm:
            return

        deleted = self.be.delete_password(website)
        if deleted:
            self.clear()
            messagebox.showinfo(title='تم الحذف', message='تم حذف البيانات بنجاح')
        else:
            messagebox.showinfo(title='غير موجود', message='لم نجد بيانات لهذا الموقع')

    def clear(self):
        self.website_var.set('')
        self.email_var.set('')
        self.password_var.set('')
        self.password_entry.config(show='*')
        self.website_entry.focus()


def main():
    main_window = Tk()
    PasswordManagerGUI(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    main()