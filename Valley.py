Option Explicit

' === 메인 진입점 ===
Sub Run_KoreaExchange_IRS_Process()
    Dim macroWb As Workbook
    Dim macroWs As Worksheet
    Dim posWs As Worksheet
    
    Set macroWb = ThisWorkbook
    Set macroWs = macroWb.Worksheets("Macro")
    Set posWs = macroWb.Worksheets("Pos")
    
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    
    ' 1단계: 외부 파일에서 Korea Exchange + IRS만 Pos시트에 가져오기
    Call Load_Pos_From_KoreaExchange_IRS(macroWs, posWs)
    
    ' 2단계: Pos시트에서 CD/KOFR 개수 세어서 Macro시트에 쓰기
    Call Count_CD_KOFR(macroWs, posWs)
    
CleanExit:
    Application.ScreenUpdating = True
    Application.EnableEvents = True
End Sub

' === 1단계: Macro!E5 경로의 파일에서 "Korea Exchange" & "IRS" 행만 Pos시트에 저장 ===
Private Sub Load_Pos_From_KoreaExchange_IRS(ByVal macroWs As Worksheet, ByVal posWs As Worksheet)
    Dim filePath As String
    Dim dataWb As Workbook
    Dim srcWs As Worksheet
    Dim lastRow As Long
    Dim srcRow As Long
    Dim destRow As Long
    
    filePath = Trim$(macroWs.Range("E5").Value)
    If filePath = "" Then
        MsgBox "Macro 시트 E5에 파일 경로가 없습니다.", vbExclamation
        Exit Sub
    End If
    
    ' 경로 존재 확인
    If Dir(filePath) = "" Then
        MsgBox "지정한 파일을 찾을 수 없습니다: " & vbCrLf & filePath, vbExclamation
        Exit Sub
    End If
    
    ' 외부 파일 열기 (읽기전용)
    On Error GoTo ErrOpen
    Set dataWb = Workbooks.Open(filePath, ReadOnly:=True)
    On Error GoTo 0
    
    On Error Resume Next
    Set srcWs = dataWb.Worksheets("Sheet1")
    On Error GoTo 0
    If srcWs Is Nothing Then
        MsgBox "대상 파일에 'Sheet1' 시트를 찾을 수 없습니다.", vbExclamation
        GoTo Cleanup
    End If
    
    ' Pos 시트 초기화 (원하면 헤더만 남기고 지우도록 바꿀 수 있음)
    posWs.Cells.Clear
    
    ' 헤더 복사 (1행 전체)
    srcWs.Rows(1).Copy Destination:=posWs.Rows(1)
    
    ' E열(거래상대방)에서 "Korea Exchange" 이고, F열이 "IRS" 인 행만 복사
    lastRow = srcWs.Cells(srcWs.Rows.Count, "E").End(xlUp).Row
    destRow = 2
    
    For srcRow = 2 To lastRow
        If srcWs.Cells(srcRow, "E").Value = "Korea Exchange" _
           And srcWs.Cells(srcRow, "F").Value = "IRS" Then
           
            srcWs.Rows(srcRow).Copy Destination:=posWs.Rows(destRow)
            destRow = destRow + 1
        End If
    Next srcRow

Cleanup:
    If Not dataWb Is Nothing Then
        dataWb.Close SaveChanges:=False
    End If
    Exit Sub
    
ErrOpen:
    MsgBox "파일을 여는 중 오류가 발생했습니다: " & vbCrLf & filePath, vbCritical
    Resume Cleanup
End Sub

' === 2단계: Pos시트의 AH/AP열에서 CD/KOFR 포함 행 개수 세기 ===
Private Sub Count_CD_KOFR(ByVal macroWs As Worksheet, ByVal posWs As Worksheet)
    Dim lastRow As Long
    Dim r As Long
    Dim valAH As String, valAP As String
    Dim cdCount As Long
    Dim kofrCount As Long
    
    ' Pos 시트 마지막 행(대략 A열 기준, 필요시 다른 기준으로 변경 가능)
    lastRow = posWs.Cells(posWs.Rows.Count, "A").End(xlUp).Row
    If lastRow < 2 Then
        ' 데이터가 없으면 0으로
        macroWs.Range("E12").Value = 0
        macroWs.Range("E13").Value = 0
        Exit Sub
    End If
    
    cdCount = 0
    kofrCount = 0
    
    For r = 2 To lastRow
        valAH = CStr(posWs.Cells(r, "AH").Value)
        valAP = CStr(posWs.Cells(r, "AP").Value)
        
        ' CD 개수 (둘 중 하나에만 있어도 카운트)
        If ContainsWord(valAH, "CD") Or ContainsWord(valAP, "CD") Then
            cdCount = cdCount + 1
        End If
        
        ' KOFR 개수 (둘 중 하나에만 있어도 카운트)
        If ContainsWord(valAH, "KOFR") Or ContainsWord(valAP, "KOFR") Then
            kofrCount = kofrCount + 1
        End If
    Next r
    
    ' Macro 시트에 쓰기
    macroWs.Range("E12").Value = cdCount
    macroWs.Range("E13").Value = kofrCount
End Sub

' === 단어 단위로 포함 여부 확인 함수 (대소문자 무시) ===
Private Function ContainsWord(ByVal text As String, ByVal word As String) As Boolean
    Dim temp As String
    Dim target As String
    
    temp = " " & UCase$(text) & " "
    target = " " & UCase$(word) & " "
    
    ' 띄어쓰기 기준으로 독립된 단어를 찾는다.
    ' ex) "KRW CD", "CD + 0.05", "KOFR + Quarterly 3M" 등
    ContainsWord = (InStr(1, temp, target, vbTextCompare) > 0)
End Function
