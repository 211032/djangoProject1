from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from medical_care_system.models import Employee, shiiregyousha
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request, error_meessage=None):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            employee = Employee.objects.get(empid=username, emppasswd=password)
            request.session['empid'] = employee.empid  # ログイン成功時にempidをセッションに保存

            if employee.emprole == 0:
                return render(request, 'home.html')
            elif employee.emprole == 1:
                return render(request, 'reception_home.html')
            elif employee.emprole == 2:
                return render(request, 'docdor_home.html')
        except Employee.DoesNotExist:
            error_message = "ユーザが見つかりません"
        return render(request, 'error.html',{'error_message': error_meessage})

    return render(request, 'login.html') #ログアウト画面

def home(request):
    return render(request,'gamen/employee/employee_home.html')
def shiire_home(request):
    return render(request,'gamen/shiiregyousha/shiire_home.html')

def employee_registration(request):
    # 従業員登録ページにリダイレクト
    if request.method == 'POST':
        empid = request.POST['empid']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        emprole = request.POST['emprole']

        # エラーチェック
        if password != confirm_password:
            messages.error(request, "パスワードが一致しません。")
            return render(request, 'gamen/employee/employee.html')

        if Employee.objects.filter(empid=empid).exists():
            messages.error(request, "このユーザーIDは既に存在しています。")
            return render(request, 'gamen/employee/employee.html')

        # 従業員の登録
        Employee.objects.create(
            empid=empid,
            empfname=first_name,
            emplname=last_name,
            emppasswd=password,
            emprole=emprole
        )
        messages.success(request, "従業員が正常に登録されました。")
        return redirect('employee_registration')

    return render(request, 'gamen/employee/employee.html')

def employee_update(request):
    if request.method == 'POST':
        empid = request.POST['empid']

        try:
            employee = Employee.objects.get(empid=empid)
            return render(request, 'gamen/employee/employee_update_form.html', {'employee': employee})
        except Employee.DoesNotExist:
            messages.error(request, "ユーザーが見つかりません。")
            return render(request, 'gamen/employee/employee_update_search.html')

    return render(request, 'gamen/employee/employee_update_search.html')

def employee_update_form(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not first_name and not last_name:
            messages.error(request, "姓または名のいずれかを入力してください。")
            return render(request, 'gamen/employee/employee_update_form.html', {'empid': empid})

        employee = get_object_or_404(Employee, empid=empid)

        if first_name:
            employee.empfname = first_name
        if last_name:
            employee.emplname = last_name

        employee.save()
        messages.success(request, "従業員情報が正常に更新されました。")
        return redirect('employee_update')

    return render(request, 'gamen/employee/employee_update_form.html')


def change_password(request):
    # セッションからユーザー情報を取得
    empid = request.session.get('empid')

    # リクエストから現在のユーザーを取得
    current_user = get_object_or_404(Employee, empid=empid)

    if request.method == 'POST':
        # パスワードを変更する従業員を特定
        employee = current_user if current_user.emprole != 0 else get_object_or_404(Employee, empid=request.POST['empid'])

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "パスワードが一致しません。")
            if current_user.emprole == 0:
                return render(request, 'gamen/employee/change_password_admin.html', {'employee': employee})
            else:
                return render(request, 'gamen/employee/change_password.html')

        employee.emppasswd = password
        employee.save()
        messages.success(request, "パスワードが正常に変更されました。")
        if current_user.emprole == 0:
            return redirect('home')
        else:
            return redirect('employee_home')

    if current_user.emprole == 0:
        return render(request, 'gamen/employee/change_password_admin.html')
    else:
        return render(request, 'gamen/employee/change_password.html')

def shiire_registration(request):
    if request.method == 'POST':
        shiireid = request.POST.get('shiireid')
        shiiremei = request.POST.get('shiiremei')
        shiireaddress = request.POST.get('shiireaddress')
        shiiretel = request.POST.get('shiiretel')
        shiirehonkin = request.POST.get('shiirehonkin')
        nouki = request.POST.get('nouki')

        # エラーチェックを行う
        errors = []

        if not shiireid:
            errors.append('仕入れ先 ID を入力してください。')
        if not shiiremei:
            errors.append('仕入れ先名 を入力してください。')
        if not shiireaddress:
            errors.append('仕入れ先住所 を入力してください。')
        if not shiiretel:
            errors.append('仕入れ先電話番号 を入力してください。')
        if not shiirehonkin:
            errors.append('資本金 を入力してください。')
        if not nouki:
            errors.append('納期 を入力してください。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

        if shiiregyousha.objects.filter(shiireid=shiireid).exists():
            messages.error(request, "この仕入れ先 ID は既に存在しています。")
            return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

        # Shiiregyousha オブジェクトを作成
        shiiregyousha.objects.create(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shiirehonkin=shiirehonkin,
            nouki=nouki
        )
        messages.success(request, '仕入れ先が正常に登録されました。')
        return redirect('shiire_registration')

    return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

def shiire_list(request, shiiregyousha=None):

    shiiregyousha = shiiregyousha.objects.all()
    for shiiregyousha in shiiregyousha:  # 変数名を複数形に変更し、ループ内で個々の仕入れ先を取り出すよう修正
        print(f"仕入れ先ID:{shiiregyousha.shiireid}, 仕入れ先名:{shiiregyousha.shiiremei}, 住所:{shiiregyousha.shiireaddress}, 電話番号:{shiiregyousha.shiiretel}, 資本金:{shiiregyousha.shiirehonkin}, 納期:{shiiregyousha.nouki}")
    return render(request, 'gamen/shiiregyousha/shiire_list.html', {'shiiregyousha': shiiregyousha})
