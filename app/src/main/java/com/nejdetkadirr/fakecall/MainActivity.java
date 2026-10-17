package com.nejdetkadirr.fakecall;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    EditText callerName, callerNumber;
    LinearLayout historyBox;
    static final String PREF = "fake_call_history";
    int dp(int n) { return (int)(n * getResources().getDisplayMetrics().density + 0.5f); }
    TextView label(String s, int size) {
        TextView t = new TextView(this); t.setText(s); t.setTextSize(size); t.setTextColor(Color.WHITE); return t;
    }
    EditText input(String hint) {
        EditText e = new EditText(this); e.setSingleLine(true); e.setHint(hint);
        e.setHintTextColor(0xffaab0ca); e.setTextColor(Color.WHITE); e.setTextSize(16);
        e.setPadding(dp(12),0,dp(12),0); e.setBackgroundColor(0xff222742); return e;
    }
    Button action(String s) {
        Button b = new Button(this); b.setText(s); b.setTextColor(Color.WHITE); b.setAllCaps(false);
        b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(0xff5959ee)); return b;
    }
    LinearLayout.LayoutParams fieldParams() {
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(-1,dp(54)); p.topMargin=dp(12); return p;
    }
    @Override public void onCreate(Bundle b) {
        super.onCreate(b); getWindow().setStatusBarColor(0xff0f1223); getWindow().setNavigationBarColor(0xff0f1223);
        ScrollView scroll=new ScrollView(this); LinearLayout root=new LinearLayout(this); root.setOrientation(1);
        root.setPadding(dp(22),dp(28),dp(22),dp(24)); root.setBackgroundColor(0xff0f1223); scroll.addView(root);
        TextView title=label("FAKE CALL",30); title.setTypeface(null,Typeface.BOLD); root.addView(title);
        TextView subtitle=label("CALL SIMULATOR  •  DEMO ONLY",12); subtitle.setTextColor(0xffaab0ca); root.addView(subtitle);
        TextView heading=label("Create a fake call",22); heading.setTypeface(null,Typeface.BOLD);
        LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(-1,-2); hp.topMargin=dp(30); root.addView(heading,hp);
        callerName=input("Caller name (e.g. Alex Morgan)"); root.addView(callerName,fieldParams());
        callerNumber=input("Phone number (optional)"); callerNumber.setInputType(3); root.addView(callerNumber,fieldParams());
        Button start=action("START FAKE CALL"); LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-1,dp(54));
        bp.topMargin=dp(14); root.addView(start,bp);
        start.setOnClickListener(v -> {
            String name=callerName.getText().toString().trim(), number=callerNumber.getText().toString().trim();
            if(name.isEmpty()) name="Unknown Caller"; if(number.isEmpty()) number="Unknown number";
            ((InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE)).hideSoftInputFromWindow(callerName.getWindowToken(),0);
            Intent i=new Intent(this,CallActivity.class); i.putExtra("name",name); i.putExtra("number",number); startActivity(i);
        });
        TextView recent=label("RECENT FAKE CALLS",16); recent.setTypeface(null,Typeface.BOLD);
        LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,-2); rp.topMargin=dp(28); root.addView(recent,rp);
        historyBox=new LinearLayout(this); historyBox.setOrientation(1); root.addView(historyBox); setContentView(scroll); loadHistory();
    }
    void loadHistory() {
        if(historyBox==null)return; historyBox.removeAllViews();
        String saved=getSharedPreferences(PREF,0).getString("items","");
        if(saved.isEmpty()){ TextView e=label("No fake calls yet.",14); e.setTextColor(0xffaab0ca); historyBox.addView(e); return; }
        for(String row:saved.split("\\n")) {
            if(row.trim().isEmpty())continue; TextView item=label(row.replace("|","  •  "),14);
            item.setPadding(dp(12),dp(14),dp(12),dp(14)); item.setBackgroundColor(0xff222742);
            LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2); p.topMargin=dp(8); historyBox.addView(item,p);
        }
    }
    @Override protected void onResume(){ super.onResume(); if(historyBox!=null)loadHistory(); }
}
