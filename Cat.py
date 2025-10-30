Sub ConcatFiles()
    Dim wb As Workbook
    Dim wsImport1 As Worksheet
    Dim wsImport2 As Worksheet
    Dim wsCurrent As Worksheet
    Dim lastRowImport1 As Long
    Dim lastRowImport2 As Long
    Dim lastColImport2 As Long
    Dim savePath As String
    Dim saveFileName As String
    Dim fullPath As String
    Dim tempWB As Workbook
    Dim tempWS As Worksheet
    Dim finalLastRow As Long  ' 추가
    
    ' 현재 워크북 설정
    Set wb = ThisWorkbook
    Set wsCurrent = wb.ActiveSheet
    
    ' Import 1과 Import 2 시트 확인
    On Error Resume Next
    Set wsImport1 = wb.Sheets("Import 1")
    Set wsImport2 = wb.Sheets("Import 2")
    On Error GoTo 0
    
    If wsImport1 Is Nothing Or wsImport2 Is Nothing Then
        MsgBox "Import 1 또는 Import 2 시트가 없습니다. 먼저 Import를 진행해주세요."
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
    
    ' ★★★ 합계 행 추가 ★★★
    ' 병합 후 마지막 행 찾기
    finalLastRow = wsImport1.Cells(wsImport1.Rows.Count, "A").End(xlUp).Row
    
    ' 마지막 행 다음에 합계 추가
    With wsImport1
        ' A컬럼에 "합계" 입력
        .Cells(finalLastRow + 1, 1).Value = "합계"
        
        ' ===== 여기서 원하는 컬럼들의 합계 추가 =====
        ' 예시: C컬럼 합계 (C6부터 마지막 행까지)
        .Cells(finalLastRow + 1, 3).Formula = "=SUM(C6:C" & finalLastRow & ")"
        
        ' 예시: D컬럼 합계 (D6부터 마지막 행까지)
        .Cells(finalLastRow + 1, 4).Formula = "=SUM(D6:D" & finalLastRow & ")"
        
        ' 예시: E컬럼 합계 (E6부터 마지막 행까지)
        .Cells(finalLastRow + 1, 5).Formula = "=SUM(E6:E" & finalLastRow & ")"
        
        ' ★ 필요한 컬럼 추가하려면 위 패턴 복사 ★
        ' .Cells(finalLastRow + 1, 컬럼번호).Formula = "=SUM(컬럼명6:컬럼명" & finalLastRow & ")"
        
        ' 수식을 값으로 변환 (CSV 저장을 위해)
        .Rows(finalLastRow + 1).Value = .Rows(finalLastRow + 1).Value
    End With
    
    ' 저장 경로 가져오기 (현재 시트의 A3 셀)
    savePath = wsCurrent.Range("A3").Value
    
    ' 경로가 비어있거나 유효하지 않은 경우 처리
    If savePath = "" Then
        MsgBox "A3 셀에 저장 경로를 입력해주세요."
        Exit Sub
    End If
    
    ' 경로 끝에 백슬래시 추가 (필요한 경우)
    If Right(savePath, 1) <> "\" Then
        savePath = savePath & "\"
    End If
    
    ' 파일명 설정
    saveFileName = "abc.csv"
    ' Import 1 파일명으로 저장하려면 아래 주석 해제
    ' saveFileName = Import1FileName & ".csv"
    
    fullPath = savePath & saveFileName
    
    ' 새 워크북 생성하여 CSV로 저장
    Set tempWB = Workbooks.Add
    Set tempWS = tempWB.Sheets(1)
    
    ' Import 1의 전체 데이터를 새 워크북으로 복사 (병합된 데이터 + 합계 포함)
    wsImport1.UsedRange.Copy
    tempWS.Range("A1").PasteSpecial xlPasteAll
    Application.CutCopyMode = False
    
    ' CSV로 저장 - 한글을 위해 UTF-8 사용
    Application.DisplayAlerts = False
    
    On Error Resume Next
    tempWB.SaveAs Filename:=fullPath, FileFormat:=62  ' 62 = xlCSVUTF8
    
    If Err.Number <> 0 Then
        Err.Clear
        tempWB.SaveAs Filename:=fullPath, FileFormat:=6, Local:=True  ' 6 = xlCSV
    End If
    On Error GoTo 0
    
    tempWB.Close SaveChanges:=False
    Application.DisplayAlerts = True
    
    MsgBox "파일이 성공적으로 저장되었습니다." & vbNewLine & _
           "경로: " & fullPath
End Sub
