from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from medical_care_system.models import Employee, shiiregyousha, patient, medicine, Treatment, Tabyouin
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ValidationError

def login(request, error_meessage=None):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            employee = Employee.objects.get(empid=username, emppasswd=password)
            request.session['empid'] = employee.empid  # ログイン成功時にempidをセッションに保存
            request.session['emprole'] = employee.emprole

            if employee.emprole == 0:
                return render(request, 'home.html')
            elif employee.emprole == 1:
                return render(request, 'reception_home.html')
            elif employee.emprole == 2:
                return render(request, 'docdor_home.html')
        except Employee.DoesNotExist:
            print(error_meessage)
        return render(request, 'error.html',{'error_message': error_meessage})

    return render(request, 'login.html') #ログアウト画面

def home(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    return render(request,'home.html')
def shiire_home(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    return render(request,'gamen/shiiregyousha/shiire_home.html')
def reception_home(request):
    if 'empid' not in request.session or request.session.get('emprole') != 1:
        return redirect('login')
    return render(request,'reception_home.html')


def employee_registration(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
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
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
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
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
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
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    # セッションからユーザー情報を取得
    empid = request.session.get('empid')

    # リクエストから現在のユーザーを取得
    current_user = get_object_or_404(Employee, empid=empid)

    if request.method == 'POST':
        # 入力されたempidがデータベースに存在するか確認
        try:
            employee = Employee.objects.get(empid=request.POST['empid'])
        except Employee.DoesNotExist:
            messages.error(request, "入力されたIDは存在しません。")
            return render(request, 'gamen/employee/change_password_admin.html')

        # 管理者以外の場合はエラーメッセージを表示し、現在のページに戻る
        if current_user.emprole != 0:
            messages.error(request, "このユーザーはパスワードを変更する権限がありません。")
            return render(request, 'gamen/employee/change_password_admin.html', {'employee': employee})

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "パスワードが一致しません。")
            return render(request, 'gamen/employee/change_password_admin.html', {'employee': employee})

    return render(request, 'gamen/employee/change_password_admin.html')

import re

def shiire_registration(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
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
        elif not re.match(r'^[0-9()\-]+$', shiiretel):
            errors.append('仕入れ先電話番号 は数字、（）、- のみを含む必要があります。')
        elif len(re.sub(r'[^0-9]', '', shiiretel)) != 11:  # 電話番号の数字が11桁であることを確認
            errors.append('仕入れ先電話番号 は11桁の数字でなければなりません。')
        if not shiirehonkin:
            errors.append('資本金 を入力してください。')
        elif not re.match(r'^[0-9,円]*$', shiirehonkin):
            errors.append('資本金 は数字、カンマ、円記号のみを含む必要があります。')
        else:
            # カンマと円記号を取り除く
            cleaned_shiirehonkin = re.sub(r'[^\d]', '', shiirehonkin)
            try:
                shiirehonkin = int(cleaned_shiirehonkin)
            except ValueError:
                errors.append('資本金 には数値のみを含む必要があります。')
        if not nouki:
            errors.append('納期 を入力してください。')
        else:
            try:
                nouki = int(nouki)
            except ValueError:
                errors.append('納期 には数字を入力してください。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

        if shiiregyousha.objects.filter(shiireid=shiireid).exists():
            messages.error(request, "この仕入れ先 ID は既に存在しています。")
            return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

        # 新しい仕入れ先情報の作成
        new_shiire = shiiregyousha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shiirehonkin=shiirehonkin,
            nouki=nouki
        )
        new_shiire.save()

        messages.success(request, '仕入れ先情報が正常に登録されました。')
        return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')

    return render(request, 'gamen/shiiregyousha/shiire_registration_home.html')




def shiire_list(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    shiiregyousha_list = shiiregyousha.objects.all()

    if not shiiregyousha_list:
        messages.error(request, "現在、登録されている仕入れ先情報はありません。")

    return render(request, 'gamen/shiiregyousha/shiire_list.html', {'shiiregyousha_list': shiiregyousha_list})


def shiire_search(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    if request.method == 'POST':
        address = request.POST.get('address')

        # 住所の一部を含む仕入れ先を検索
        shiiregyousha_list = shiiregyousha.objects.filter(shiireaddress__contains=address)

        if shiiregyousha_list.exists():
            return render(request, 'gamen/shiiregyousha/shiire_list.html', {'shiiregyousha_list': shiiregyousha_list})
        else:
            messages.info(request, "該当する仕入れ先が見つかりませんでした。")
            return render(request, 'gamen/shiiregyousha/shiire_search.html')

    return render(request, 'gamen/shiiregyousha/shiire_search.html')


def patient_registration(request):
    if 'empid' not in request.session or request.session.get('emprole') != 1:
        return redirect('login')
    if request.method == 'POST':
        patient_id = request.POST.get('patid')
        last_name = request.POST.get('patlname')
        first_name = request.POST.get('patfname')
        insurance_number = request.POST.get('hokenmei')
        expiration_date = request.POST.get('hokenexp')

        # エラーチェック
        errors = []

        if not patient_id:
            errors.append('患者IDを入力してください。')
        if not first_name:
            errors.append('姓を入力してください。')
        if not last_name:
            errors.append('名を入力してください。')
        if not insurance_number:
            errors.append('保険証記号番号を入力してください。')
        elif len(re.sub(r'[^0-9]', '', insurance_number)) != 10:  # 保険証番号が10桁であることを確認
            errors.append('保険証記号番号は10桁の数字でなければなりません。')
        if not expiration_date:
            errors.append('有効期限を入力してください。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/patient/patient_registration.html')

        # 患者の登録
        patient.objects.create(
            patid=patient_id,
            patlname=last_name,
            patfname=first_name,
            hokenmei=insurance_number,
            hokenexp=expiration_date
        )
        messages.success(request, '患者が正常に登録されました。')
        return redirect('patient_registration')

    return render(request, 'gamen/patient/patient_registration.html')

def patient_insurance_change(request):
    if 'empid' not in request.session or request.session.get('emprole') != 1:
        return redirect('login')
    empid = request.session.get('empid')
    current_user = get_object_or_404(Employee, empid=empid)

    if request.method == 'POST':
        patid = request.POST.get('patid')
        patlname = request.POST.get('patfname')
        patfname = request.POST.get('patlname')
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        # 入力値の検証
        errors = []
        if not patid:
            errors.append('患者IDを入力してください。')
        if not patfname:
            errors.append('名を入力してください。')
        if not patlname:
            errors.append('姓を入力してください。')
        if not hokenmei and not hokenexp:
            errors.append('保険証記号番号または有効期限を入力してください。')
        if hokenmei and len(re.sub(r'[^0-9]', '', hokenmei)) != 10:  # 保険証番号が10桁であることを確認
            errors.append('保険証記号番号は10桁の数字でなければなりません。')

        # 患者がデータベースに存在するか確認
        try:
            patient_instance = patient.objects.get(patid=patid)
        except patient.DoesNotExist:
            errors.append('指定された患者IDは存在しません。')
            patient_instance = None

        if patient_instance:
            current_hokenexp = patient_instance.hokenexp

            # 新しい有効期限が現在の有効期限より古いか同じ場合を確認
            if hokenexp:
                try:
                    new_hokenexp_date = datetime.strptime(hokenexp, '%Y-%m-%d').date()
                    if new_hokenexp_date <= current_hokenexp:
                        errors.append('有効期限は現在の期限よりも新しい日付でなければなりません。')
                except ValueError:
                    errors.append('有効期限は有効な日付形式である必要があります（YYYY-MM-DD）。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/patient/insurance_change.html')

        if patient_instance:
            # 患者情報の更新
            if patfname:
                patient_instance.patfname = patfname
            if patlname:
                patient_instance.patlname = patlname
            if hokenmei:
                patient_instance.hokenmei = hokenmei
            if hokenexp:
                patient_instance.hokenexp = hokenexp
            patient_instance.save()

            messages.success(request, '患者情報が正常に変更されました。')
            return redirect('patient_insurance_change')

    return render(request, 'gamen/patient/insurance_change.html')

def patient_search(request):
    if 'empid' not in request.session or request.session.get('emprole') != 1:
        return redirect('login')
    patients = None
    if request.method == 'POST':
        patfname = request.POST.get('patfname').strip()
        patlname = request.POST.get('patlname').strip()

        # 検索条件を構築
        search_criteria = Q()
        if patfname:
            search_criteria |= Q(patfname__icontains=patfname)
        if patlname:
            search_criteria |= Q(patlname__icontains=patlname)

        # 検索を実行
        if search_criteria:
            patients = patient.objects.filter(search_criteria)

            # 全ての条件に一致する患者の検索
            exact_criteria = Q()
            if patfname:
                exact_criteria &= Q(patfname__iexact=patfname)
            if patlname:
                exact_criteria &= Q(patlname__iexact=patlname)

            exact_patients = patient.objects.filter(exact_criteria)

            # 条件の一部に一致するが全てには一致しない場合にエラーメッセージを表示
            if patients.exists() and not exact_patients.exists():
                messages.error(request, "一部の条件に一致しましたが、完全に一致する患者はいませんでした。")

    return render(request, 'gamen/patient/patient_search.html', {'patients': patients})

def patients(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    query = request.GET.get('q')
    error_message = None
    if query:
        patients = patient.objects.filter(Q(patid__icontains=query) | Q(patfname__icontains=query) | Q(patlname__icontains=query))
        if not patients:
            error_message = "該当する患者が見つかりませんでした。"
    else:
        patients = patient.objects.all()
    return render(request, 'gamen/medicine/patients.html', {'patients': patients, 'error_message': error_message})



def doctor_home(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    return render(request, 'docdor_home.html')



def prescribe_medicine(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    empid = request.session.get('empid')
    current_user = get_object_or_404(Employee, empid=empid)

    if request.method == 'POST':
        patid = request.POST.get('patid')
        medicineid = request.POST.get('medicineid')
        dosage = request.POST.get('dosage')

        if not patid or not medicineid or not dosage:
            messages.error(request, 'すべてのフィールドを入力してください。')
            return redirect('prescribe_medicine')

        try:
            patient_instance = get_object_or_404(patient, patid=patid)
            medicine_instance = get_object_or_404(medicine, medicineid=medicineid)
        except:
            messages.error(request, '患者または薬剤が存在しません。')
            return redirect('prescribe_medicine')

        # Store the prescription data in the session
        prescription = {
            'empid': current_user.empid,
            'patid': patient_instance.patid,
            'medicineid': medicine_instance.medicineid,
            'dosage': dosage,
            'patient_name': f'{patient_instance.patlname} {patient_instance.patfname}',
            'medicine_name': medicine_instance.medicinename
        }
        if 'prescriptions' not in request.session:
            request.session['prescriptions'] = []
        request.session['prescriptions'].append(prescription)
        request.session.modified = True

        return redirect('prescription_list')

    medicines = medicine.objects.all()
    return render(request, 'gamen/Treatment/prescribe_medicine.html', {'medicines': medicines})

def prescription_list(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    if request.method == 'POST':
        action = request.POST.get('action')
        index = int(request.POST.get('index', -1))
        if action == 'confirm_all':
            return redirect('confirm_prescription')
        elif action == 'confirm' and index >= 0:
            request.session['confirm_prescription'] = request.session['prescriptions'][index]
            request.session['confirm_prescription_index'] = index
            return redirect('confirm_prescription')
        elif action == 'delete' and index >= 0:
            prescriptions = request.session.get('prescriptions', [])
            if index < len(prescriptions):
                del prescriptions[index]
                request.session['prescriptions'] = prescriptions
                request.session.modified = True
                messages.info(request, '処方が削除されました。')

    prescriptions = request.session.get('prescriptions', [])
    return render(request, 'gamen/Treatment/prescription_list.html', {'prescriptions': prescriptions})

def confirm_prescription(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    prescriptions = request.session.get('prescriptions', [])
    if not prescriptions:
        messages.error(request, '処置情報がありません。')
        return redirect('prescribe_medicine')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm_all':
            for prescription in prescriptions:
                Treatment.objects.create(
                    empid_id=prescription['empid'],
                    patid_id=prescription['patid'],
                    medicineid_id=prescription['medicineid'],
                    dosage=prescription['dosage'],
                    status='confirmed'
                )
            messages.success(request, 'すべての処置が確定されました。')
            request.session['prescriptions'] = []
            request.session.modified = True
        elif action == 'edit':
            return redirect('prescription_list')

    return render(request, 'gamen/Treatment/confirm_prescription.html', {'prescriptions': prescriptions})


def treatment_history(request):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    empid = request.session.get('empid')
    current_user = get_object_or_404(Employee, empid=empid)

    treatments = Treatment.objects.all()

    if request.method == 'POST':
        patid = request.POST.get('patid')
        try:
            patient_instance = patient.objects.get(patid=patid)
        except patient.DoesNotExist:
            messages.error(request, "該当する患者が見つかりませんでした。")
            return redirect('treatment_history')

        return redirect('treatment_history_results', patid=patid)

    return render(request, 'gamen/Treatment/treatment_history.html', {'treatments': treatments})






def treatment_history_results(request, patid):
    if 'empid' not in request.session or request.session.get('emprole') != 2:
        return redirect('login')
    empid = request.session.get('empid')
    current_user = get_object_or_404(Employee, empid=empid)

    patient_instance = get_object_or_404(patient, patid=patid)
    treatments = Treatment.objects.filter(patid=patient_instance)

    if not treatments.exists():
        messages.info(request, "該当患者に処置履歴がありません。")

    return render(request, 'gamen/Treatment/treatment_history_results.html', {'patient': patient_instance, 'treatments': treatments})

def tabyouin_home(request):
    return render(request, 'gamen/tabyouin/tabyouin_home.html')

def tabyouin_registration(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    if request.method == 'POST':
        tabyouinid = request.POST.get('tabyouinid')
        tabyouinmei = request.POST.get('tabyouinmei')
        tabyouinaddress = request.POST.get('tabyouinaddress')
        tabyouintel = request.POST.get('tabyouintel')
        tabyouinshihonkin = request.POST.get('tabyouinshihonkin')
        kyukyu = request.POST.get('kyukyu')

        # 入力データのバリデーション
        errors = []
        if not tabyouinid:
            errors.append('他病院 ID を入力してください。')
        if not tabyouinmei:
            errors.append('他病院名 を入力してください。')
        if not tabyouinaddress:
            errors.append('他病院住所 を入力してください。')
        if not tabyouintel:
            errors.append('他病院電話番号 を入力してください。')
        elif not re.match(r'^[0-9()\-]+$', tabyouintel):
            errors.append('他病院電話番号 は数字、（）、- のみを含む必要があります。')
        elif len(re.sub(r'[^0-9]', '', tabyouintel)) < 11:  # 電話番号の数字が11文字以上であることを確認
            errors.append('他病院電話番号 は11文字以上でなければなりません。')
        if not tabyouinshihonkin:
            errors.append('資本金 を入力してください。')
        elif not re.match(r'^[0-9,円]+$', tabyouinshihonkin):
            errors.append('資本金 は数字、カンマ、円記号のみを含む必要があります。')
        else:
            tabyouinshihonkin = re.sub(r'[円,]', '', tabyouinshihonkin)  # 円記号とカンマを削除

        if not kyukyu:
            errors.append('救急対応を選択してください。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/tabyouin/tabyouin_registration.html')

        if Tabyouin.objects.filter(tabyouinid=tabyouinid).exists():
            messages.error(request, 'この他病院 ID は既に存在しています。')
            return render(request, 'gamen/tabyouin/tabyouin_registration.html')

        # 他病院の登録
        try:
            new_tabyouin = Tabyouin(
                tabyouinid=tabyouinid,
                tabyouinmei=tabyouinmei,
                tabyouinaddress=tabyouinaddress,
                tabyouintel=tabyouintel,
                tabyouinshihonkin=int(tabyouinshihonkin),
                kyukyu=int(kyukyu)
            )
            new_tabyouin.save()
            messages.success(request, '他病院が正常に登録されました。')
            return redirect('tabyouin_list')
        except Exception as e:
            messages.error(request, '登録にエラーが発生しました。再度入力してください。')

    return render(request, 'gamen/tabyouin/tabyouin_registration.html')

def tabyouin_list(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    tabyouin_list = Tabyouin.objects.all()
    if not tabyouin_list:
        messages.error(request, "現在、登録されている他病院情報はありません。")
    return render(request, 'gamen/tabyouin/tabyouin_list.html', {'tabyouin_list': tabyouin_list})

def tabyouin_search(request):
    tabyouin_list = Tabyouin.objects.all()

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()

        if address:
            tabyouin_list = Tabyouin.objects.filter(tabyouinaddress__icontains=address)
            if not tabyouin_list.exists():
                messages.error(request, "該当する他病院が見つかりませんでした。")

    return render(request, 'gamen/tabyouin/tabyouin_search.html', {'tabyouin_list': tabyouin_list})

def tabyouin_update(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    tabyouin_list = Tabyouin.objects.all()

    if request.method == 'POST':
        tabyouinid = request.POST.get('tabyouinid', '').strip()
        try:
            tabyouin = Tabyouin.objects.get(tabyouinid=tabyouinid)
            return render(request, 'gamen/tabyouin/tabyouin_update_form.html', {'tabyouin': tabyouin})
        except Tabyouin.DoesNotExist:
            messages.error(request, "指定された他病院IDは存在しません。")
            return render(request, 'gamen/tabyouin/tabyouin_update_search.html', {'tabyouin_list': tabyouin_list})

    return render(request, 'gamen/tabyouin/tabyouin_update_search.html', {'tabyouin_list': tabyouin_list})

def tabyouin_update_confirm(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    if request.method == 'POST':
        tabyouinid = request.POST.get('tabyouinid')
        tabyouintel = request.POST.get('tabyouintel')

        errors = []

        if not tabyouintel:
            errors.append('他病院電話番号 を入力してください。')
        elif not re.match(r'^[0-9()\-]+$', tabyouintel):
            errors.append('他病院電話番号 は数字、（）、- のみを含む必要があります。')
        elif len(re.sub(r'[^0-9]', '', tabyouintel)) < 11:
            errors.append('他病院電話番号 は11文字以上でなければなりません。')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'gamen/tabyouin/tabyouin_update_form.html', {'tabyouinid': tabyouinid, 'tabyouintel': tabyouintel})

        return render(request, 'gamen/tabyouin/tabyouin_update_confirm.html', {'tabyouinid': tabyouinid, 'tabyouintel': tabyouintel})

    return redirect('tabyouin_update_search')

def tabyouin_update_save(request):
    if 'empid' not in request.session or request.session.get('emprole') != 0:
        return redirect('login')
    if request.method == 'POST':
        tabyouinid = request.POST.get('tabyouinid')
        tabyouintel = request.POST.get('tabyouintel')

        try:
            tabyouin = Tabyouin.objects.get(tabyouinid=tabyouinid)
            tabyouin.tabyouintel = tabyouintel
            tabyouin.save()
            messages.success(request, '他病院情報が正常に更新されました。')
            return redirect('tabyouin_list')
        except Tabyouin.DoesNotExist:
            messages.error(request, "指定された他病院IDは存在しません。")
            return redirect('tabyouin_update_search')

    return redirect('tabyouin_update_search')

def kanja_home(request):
    return render(request, 'gamen/kanja/kanja_home.html')


def kanja_login(request):
    error_message = None  # エラーメッセージの初期化

    if request.method == "POST":
        patid = request.POST.get("patid")
        hokenmei = request.POST.get("hokenmei")

        if patid and hokenmei:
            try:
                # `patid` で患者を取得
                user = patient.objects.get(patid=patid)
                # `hokenmei` が一致するか確認
                if user.hokenmei == hokenmei:
                    # ログイン成功時に patid をセッションに保存
                    request.session['patid'] = user.patid
                    return redirect("kanja_home")  # メニュー画面へリダイレクト
                else:
                    error_message = "保険証名記号番号が正しくありません"
            except patient.DoesNotExist:
                error_message = "患者IDが存在しません"
        else:
            error_message = "全てのフィールドを入力してください"

    return render(request, "kanja_login.html", {"error_message": error_message})


def kanjahukuyou_list(request):
    # セッションから患者IDを取得します
    patid = request.session.get('patid')

    # 患者IDがセッションに存在しない場合、ログイン画面にリダイレクトします
    if not patid:
        messages.error(request, "患者IDが見つかりません。ログインし直してください。")
        return redirect('kanja_login')

    # 患者のインスタンスを取得します
    patient_instance = get_object_or_404(patient, patid=patid)

    # ログインしている患者の治療履歴を取得します
    treatments = Treatment.objects.filter(patid=patient_instance).select_related('medicineid')

    # 治療履歴が存在しない場合、メッセージを表示して画面に戻します
    if not treatments.exists():
        messages.info(request, "該当患者に処方履歴がありません。")
        return render(request, 'gamen/kanja/kanjahukuyou_list.html', {'treatments': None})

    # 各治療データに対して、薬剤ID、薬剤名、投与量をリストにまとめます
    treatment_data = []
    for treatment in treatments:
        treatment_data.append({
            'medicineid': treatment.medicineid.medicineid,
            'medicinename': treatment.medicineid.medicinename,
            'dosage': treatment.dosage,
        })

    # テンプレートに治療データを渡して表示します
    return render(request, 'gamen/kanja/kanjahukuyou_list.html', {'treatments': treatment_data})


def kanjahukuyou(request):
    # セッションから患者IDを取得
    patid = request.session.get('patid')

    # 患者IDがセッションにない場合、ログイン画面へリダイレクト
    if not patid:
        messages.error(request, "患者IDが見つかりません。ログインし直してください。")
        return redirect('kanja_login')

    # 患者のインスタンスを取得
    patient_instance = get_object_or_404(patient, patid=patid)

    # 患者の治療履歴（処方）を取得
    treatments = Treatment.objects.filter(patid=patient_instance).select_related('medicineid')

    # 治療履歴がない場合の処理
    if not treatments.exists():
        messages.info(request, "該当患者に処方履歴がありません。")
        return render(request, 'gamen/kanja/kanjahukuyou.html', {'treatments': None})

    # POSTリクエストが送られた場合の処理（服用処理）
    if request.method == 'POST':
        # POSTから治療IDと服用量を取得
        treatment_id = request.POST.get('treatment_id')
        taken_dosage = int(request.POST.get('taken_dosage'))

        # 指定された治療を取得
        treatment = get_object_or_404(Treatment, treatment_id=treatment_id, patid=patient_instance)

        # `hukuyou_dosage` フィールドに服用量を加算する処理
        treatment.hukuyou_dosage += taken_dosage  # 患者が服用した量を加算
        treatment.taken_at = datetime.now()  # 服用日時を更新
        treatment.save()

        messages.success(request, f'{treatment.medicineid.medicinename} を {taken_dosage} 服用しました。')

    # テンプレートに渡す治療データを準備
    treatment_data = []
    for treatment in treatments:
        treatment_data.append({
            'treatment_id': treatment.treatment_id,
            'medicineid': treatment.medicineid.medicineid,
            'medicinename': treatment.medicineid.medicinename,
            'dosage': treatment.dosage,  # 医師が処方した量
            'hukuyou_dosage': treatment.hukuyou_dosage,  # 患者が実際に服用した量
            'taken_at': treatment.taken_at,
        })

    # テンプレートに治療データを渡して表示
    return render(request, 'gamen/kanja/kanjahukuyou.html', {'treatments': treatment_data})
