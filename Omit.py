Option Explicit
' 전역 변수로 Import 1 파일명 저장
Dim Import1FileName As String

' ★★★ 전체 자동 실행 매크로 ★★★
Sub RunAllProcess()
    Dim macroSheet As Worksheet
    Dim file1Path As String
    Dim file2Path As String
    Dim outputPath As String
    Dim dateValue As String
    
    ' Macro 시트 설정
    Set macroSheet = ThisWorkbook.Sheets("Macro")
    
    ' 경로 가져오기
    file1Path = macroSheet.Range("C3").Value
    file2Path = macroSheet.Range("C4").Value
    outputPath = macroSheet.Range("C5").Value
    dateValue = macroSheet.Range("C8").Value
    
    ' 경로 확인
    If file1Path = "" Or file2Path = "" Or outputPath = "" Or dateValue = "" Then
        MsgBox "C3, C4, C5, C8 셀에 필요한 정보를 모두 입력해주세요."
        Exit Sub
    End If
    
    ' 1단계: Import 1 실행
    Call AutoImportFile1(file1Path)
    
    ' 2단계: Import 2 실행
    Call AutoImportFile2(file2Path)
    
    ' 3단계: Concat 및 저장
    Call AutoConcatAndSave(outputPath, dateValue)
    
    ' 4단계: ClearContents 실행
    Call ClearContents
    
    MsgBox "모든 작업이 완료되었습니다!"
End Sub

' 자동 Import 1 (파일 선택 없이)
Sub AutoImportFile1(filePath As String)
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim sourceWB As Workbook
    Dim sourceWS As Worksheet
    Dim lastRow As Long
    Dim cellB3Value As String
    
    ' 파일 존재 확인
    If Dir(filePath) = "" Then
        MsgBox "Import 1 파일을 찾을 수 없습니다: " & filePath
        Exit Sub
    End If
    
    ' 현재 워크북과 Import 1 시트 설정
    Set wb = ThisWorkbook
    
    ' Import 1 시트가 없으면 생성
    On Error Resume Next
    Set ws = wb.Sheets("Import 1")
    If ws Is Nothing Then
        Set ws = wb.Sheets.Add
        ws.Name = "Import 1"
    End If
    On Error GoTo 0
    
    ' 기존 데이터 클리어
    ws.Cells.Clear
    
    ' CSV 파일 열기
    Set sourceWB = Workbooks.Open(Filename:=filePath, Local:=True)
    Set sourceWS = sourceWB.Sheets(1)
    
    ' B3 셀 값 확인
    cellB3Value = Trim(sourceWS.Range("B3").Value)
    
    ' A7부터 데이터가 있는 마지막 행 찾기
    lastRow = sourceWS.Cells(sourceWS.Rows.Count, "A").End(xlUp).Row
    
    ' B3 값에 따라 AF 컬럼 처리
    If cellB3Value = "CD IRS" Then
        sourceWS.Range("AF7:AF" & lastRow).Value = "CD"
        sourceWS.Range("AF6").Value = "Reference Rate"
        
    ElseIf cellB3Value = "KOFR IRS" Then
        sourceWS.Range("AF7:AF" & lastRow).Value = "KOFR"
        sourceWS.Range("AF6").Value = "Reference Rate"
    End If
    
    ' 전체 데이터를 Import 1 시트로 복사
    sourceWS.UsedRange.Copy
    ws.Range("A1").PasteSpecial xlPasteAll
    Application.CutCopyMode = False
    
    ' 소스 워크북 닫기
    sourceWB.Close SaveChanges:=False
End Sub

' 자동 Import 2 (파일 선택 없이)
Sub AutoImportFile2(filePath As String)
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim sourceWB As Workbook
    Dim sourceWS As Worksheet
    Dim lastRow As Long
    Dim cellB3Value As String
    
    ' 파일 존재 확인
    If Dir(filePath) = "" Then
        MsgBox "Import 2 파일을 찾을 수 없습니다: " & filePath
        Exit Sub
    End If
    
    ' 현재 워크북과 Import 2 시트 설정
    Set wb = ThisWorkbook
    
    ' Import 2 시트가 없으면 생성
    On Error Resume Next
    Set ws = wb.Sheets("Import 2")
    If ws Is Nothing Then
        Set ws = wb.Sheets.Add
        ws.Name = "Import 2"
    End If
    On Error GoTo 0
    
    ' 기존 데이터 클리어
    ws.Cells.Clear
    
    ' CSV 파일 열기
    Set sourceWB = Workbooks.Open(Filename:=filePath, Local:=True)
    Set sourceWS = sourceWB.Sheets(1)
    
    ' B3 셀 값 확인
    cellB3Value = Trim(sourceWS.Range("B3").Value)
    
    ' A7부터 데이터가 있는 마지막 행 찾기
    lastRow = sourceWS.Cells(sourceWS.Rows.Count, "A").End(xlUp).Row
    
    ' B3 값에 따라 AF 컬럼 처리
    If cellB3Value = "CD IRS" Then
        sourceWS.Range("AF7:AF" & lastRow).Value = "CD"
        sourceWS.Range("AF6").Value = "Reference Rate"
        
    ElseIf cellB3Value = "KOFR IRS" Then
        sourceWS.Range("AF7:AF" & lastRow).Value = "KOFR"
        sourceWS.Range("AF6").Value = "Reference Rate"
    End If
    
    ' 전체 데이터를 Import 2 시트로 복사
    sourceWS.UsedRange.Copy
    ws.Range("A1").PasteSpecial xlPasteAll
    Application.CutCopyMode = False
    
    ' 소스 워크북 닫기
    sourceWB.Close SaveChanges:=False
End Sub

' 자동 Concat 및 저장
Sub AutoConcatAndSave(outputPath As String, dateValue As String)
    Dim wb As Workbook
    Dim wsImport1 As Worksheet
    Dim wsImport2 As Worksheet
    Dim lastRowImport1 As Long
    Dim lastRowImport2 As Long
    Dim lastColImport2 As Long
    Dim saveFileName As String
    Dim fullPath As String
    Dim tempWB As Workbook
    Dim tempWS As Worksheet
    Dim finalLastRow As Long
    
    ' 현재 워크북 설정
    Set wb = ThisWorkbook
    
    ' Import 1과 Import 2 시트 확인
    On Error Resume Next
    Set wsImport1 = wb.Sheets("Import 1")
    Set wsImport2 = wb.Sheets("Import 2")
    On Error GoTo 0
    
    If wsImport1 Is Nothing Or wsImport2 Is Nothing Then
        MsgBox "Import 1 또는 Import 2 시트가 없습니다."
        Exit Sub
    End If
    
    ' Import 1의 마지막 데이터 행 찾기
    lastRowImport1 = wsImport1.Cells(wsImport1.Rows.Count, "A").End(xlUp).Row
    
    ' Import 2의 데이터 범위 찾기 (7행부터)
    lastRowImport2 = wsImport2.Cells(wsImport2.Rows.Count, "A").End(xlUp).Row
    lastColImport2 = wsImport2.Cells(6, wsImport2.Columns.Count).End(xlToLeft).Column
    
    ' Import 2의 7행부터 마지막 행까지의 데이터를 Import 1의 마지막 행 다음에 복사
    If lastRowImport2 >= 7 Then
        wsImport2.Range(wsImport2.Cells(7, 1), wsImport2.Cells(lastRowImport2, lastColImport2)).Copy
        wsImport1.Cells(lastRowImport1 + 1, 1).PasteSpecial xlPasteAll
        Application.CutCopyMode = False
    End If
    
    ' 합계 행 추가 (필요시)
    finalLastRow = wsImport1.Cells(wsImport1.Rows.Count, "A").End(xlUp).Row
    With wsImport1
        .Cells(finalLastRow + 1, 1).Value = "합계"
        ' 필요한 컬럼 합계 추가 (예시)
        ' .Cells(finalLastRow + 1, 3).Formula = "=SUM(C6:C" & finalLastRow & ")"
        ' .Rows(finalLastRow + 1).Value = .Rows(finalLastRow + 1).Value
    End With
    
    ' 경로 끝에 백슬래시 추가
    If Right(outputPath, 1) <> "\" Then
        outputPath = outputPath & "\"
    End If
    
    ' 파일명 설정: NPV_YYYYMMDD.csv
    saveFileName = "NPV_" & dateValue & ".csv"
    fullPath = outputPath & saveFileName
    
    ' 새 워크북 생성하여 CSV로 저장
    Set tempWB = Workbooks.Add
    Set tempWS = tempWB.Sheets(1)
    
    ' Import 1의 전체 데이터를 새 워크북으로 복사
    wsImport1.UsedRange.Copy
    tempWS.Range("A1").PasteSpecial xlPasteAll
    Application.CutCopyMode = False
    
    ' CSV로 저장
    Application.DisplayAlerts = False
    
    On Error Resume Next
    tempWB.SaveAs Filename:=fullPath, FileFormat:=62  ' UTF-8 CSV
    If Err.Number <> 0 Then
        Err.Clear
        tempWB.SaveAs Filename:=fullPath, FileFormat:=6, Local:=True  ' 일반 CSV
    End If
    On Error GoTo 0
    
    tempWB.Close SaveChanges:=False
    Application.DisplayAlerts = True
End Sub

' ClearContents 매크로
Sub ClearContents()
    Dim wb As Workbook
    Dim ws As Worksheet
    
    Set wb = ThisWorkbook
    
    ' Import 1 시트 내용 클리어
    On Error Resume Next
    Set ws = wb.Sheets("Import 1")
    If Not ws Is Nothing Then
        ws.Cells.Clear
    End If
    
    ' Import 2 시트 내용 클리어
    Set ws = wb.Sheets("Import 2")
    If Not ws Is Nothing Then
        ws.Cells.Clear
    End If
    On Error GoTo 0
End Sub

' 개별 실행 버튼용 (필요시)
Sub CreateAutoButton()
    Dim ws As Worksheet
    Dim btn As Object
    
    Set ws = ThisWorkbook.Sheets("Macro")
    
    ' 자동 실행 버튼
    Set btn = ws.Buttons.Add(100, 100, 150, 30)
    With btn
        .Name = "btnRunAll"
        .Caption = "전체 프로세스 실행"
        .OnAction = "RunAllProcess"
    End With
    
    MsgBox "자동 실행 버튼이 생성되었습니다."
End Sub
