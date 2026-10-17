#!/usr/bin/env python3
from pathlib import Path

root = Path.cwd()
pkg = root / "app/src/main/java/com/nejdetkadirr/fakecall"
pkg.mkdir(parents=True, exist_ok=True)

main = r'''package com.nejdetkadirr.fakecall;
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
'''

call = r'''package com.nejdetkadirr.fakecall;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.view.Gravity;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.util.Locale;

public class CallActivity extends AppCompatActivity {
    String callerName, callerNumber;
    LinearLayout root, controls;
    TextView timerView, statusView;
    Handler handler=new Handler();
    long startedAt;
    boolean connected=false, muted=false, speaker=false, keypadShown=false, saved=false;
    static final String PREF="fake_call_history";
    int dp(int n){return (int)(n*getResources().getDisplayMetrics().density+0.5f);}
    TextView label(String s,int size){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(Color.WHITE);t.setGravity(Gravity.CENTER);return t;}
    Button button(String s,int color){Button b=new Button(this);b.setText(s);b.setTextColor(Color.WHITE);b.setAllCaps(false);b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(color));return b;}
    @Override public void onCreate(Bundle b){
        super.onCreate(b); callerName=getIntent().getStringExtra("name"); callerNumber=getIntent().getStringExtra("number");
        if(callerName==null)callerName="Unknown Caller";if(callerNumber==null)callerNumber="Unknown number";
        getWindow().setStatusBarColor(0xff101827);getWindow().setNavigationBarColor(0xff101827);showIncoming();
    }
    String initials(){
        String[] p=callerName.trim().split("\\s+"); if(p.length==0||p[0].isEmpty())return "?";
        String s=p[0].substring(0,1).toUpperCase(Locale.ROOT);
        if(p.length>1)s+=p[p.length-1].substring(0,1).toUpperCase(Locale.ROOT);return s;
    }
    void base(String status){
        root=new LinearLayout(this);root.setOrientation(1);root.setGravity(Gravity.CENTER_HORIZONTAL);root.setPadding(dp(24),dp(28),dp(24),dp(24));root.setBackgroundColor(0xff101827);setContentView(root);
        TextView brand=label("FAKE CALL SIMULATOR",12);brand.setTextColor(0xff9ca9c8);root.addView(brand,new LinearLayout.LayoutParams(-1,dp(36)));
        TextView avatar=label(initials(),30);avatar.setTypeface(null,Typeface.BOLD);avatar.setBackgroundColor(0xff4548a8);
        LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(104),dp(104));ap.topMargin=dp(48);root.addView(avatar,ap);
        TextView name=label(callerName,27);name.setTypeface(null,Typeface.BOLD);LinearLayout.LayoutParams np=new LinearLayout.LayoutParams(-1,-2);np.topMargin=dp(22);root.addView(name,np);
        TextView number=label(callerNumber,16);number.setTextColor(0xffb5bfd4);root.addView(number,new LinearLayout.LayoutParams(-1,dp(36)));
        statusView=label(status,15);statusView.setTextColor(0xffaab0ca);LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(-1,dp(38));sp.topMargin=dp(8);root.addView(statusView,sp);
    }
    void showIncoming(){
        base("Incoming fake call");LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,dp(64));rp.topMargin=dp(55);root.addView(row,rp);
        Button no=button("DECLINE",0xffd83f53),yes=button("ACCEPT",0xff24a36a);
        row.addView(no,new LinearLayout.LayoutParams(0,-1,1));row.addView(new Space(this),new LinearLayout.LayoutParams(dp(18),1));row.addView(yes,new LinearLayout.LayoutParams(0,-1,1));
        no.setOnClickListener(v->finishCall("Declined"));yes.setOnClickListener(v->showConnected());
    }
    void showConnected(){
        connected=true;startedAt=System.currentTimeMillis();base("Connected • simulated call");
        timerView=label("00:00",19);timerView.setTextColor(0xffcbd5e1);root.addView(timerView,new LinearLayout.LayoutParams(-1,dp(42)));
        controls=new LinearLayout(this);controls.setOrientation(1);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,-2);cp.topMargin=dp(25);root.addView(controls,cp);
        addRow("Mute","Keypad");addRow("Speaker Off","End Call");updateTimer();
    }
    void addRow(String left,String right){
        LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER);LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,dp(58));rp.topMargin=dp(8);controls.addView(row,rp);
        Button a=button(left,0xff374151),b=button(right,right.equals("End Call")?0xffd83f53:0xff374151);
        row.addView(a,new LinearLayout.LayoutParams(0,-1,1));row.addView(new Space(this),new LinearLayout.LayoutParams(dp(12),1));row.addView(b,new LinearLayout.LayoutParams(0,-1,1));
        if(left.equals("Mute"))a.setOnClickListener(v->{muted=!muted;a.setText(muted?"Unmute":"Mute");statusView.setText(muted?"Microphone muted • simulated":"Connected • simulated call");});
        if(left.equals("Speaker Off"))a.setOnClickListener(v->{speaker=!speaker;a.setText(speaker?"Speaker On":"Speaker Off");});
        if(right.equals("Keypad"))b.setOnClickListener(v->showKeypad());
        if(right.equals("End Call"))b.setOnClickListener(v->finishCall("Completed"));
    }
    void showKeypad(){
        keypadShown=true;base("Connected • simulated call");TextView t=label("Keypad • simulated only",18);root.addView(t,new LinearLayout.LayoutParams(-1,dp(45)));
        GridLayout grid=new GridLayout(this);grid.setColumnCount(3);String[] keys={"1","2","3","4","5","6","7","8","9","*","0","#"};
        for(String key:keys){Button k=button(key,0xff374151);GridLayout.LayoutParams gp=new GridLayout.LayoutParams();gp.width=dp(78);gp.height=dp(48);gp.setMargins(dp(5),dp(4),dp(5),dp(4));grid.addView(k,gp);k.setOnClickListener(v->statusView.setText("Pressed "+key+" • simulated"));}
        root.addView(grid);Button back=button("BACK TO CALL",0xff5959ee);LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-1,dp(52));bp.topMargin=dp(14);root.addView(back,bp);
        back.setOnClickListener(v->{keypadShown=false;showConnected();});Button end=button("END CALL",0xffd83f53);root.addView(end,new LinearLayout.LayoutParams(-1,dp(52)));end.setOnClickListener(v->finishCall("Completed"));
    }
    void updateTimer(){
        if(!connected||isFinishing())return;long sec=(System.currentTimeMillis()-startedAt)/1000;
        if(timerView!=null)timerView.setText(String.format(Locale.US,"%02d:%02d",sec/60,sec%60));handler.postDelayed(this::updateTimer,1000);
    }
    void finishCall(String result){
        if(!saved){saved=true;String row=callerName+"|"+callerNumber+"|"+result;android.content.SharedPreferences p=getSharedPreferences(PREF,0);String old=p.getString("items","");p.edit().putString("items",row+(old.isEmpty()?"":"\\n"+old)).apply();}
        connected=false;handler.removeCallbacksAndMessages(null);finish();
    }
    @Override public void onBackPressed(){finishCall(connected?"Ended":"Declined");}
    @Override protected void onDestroy(){connected=false;handler.removeCallbacksAndMessages(null);super.onDestroy();}
}
'''

(pkg / "MainActivity.java").write_text(main)
(pkg / "CallActivity.java").write_text(call)
print("Created MainActivity.java and CallActivity.java.")
print("Fake-call simulation only; no real phone calls are placed.")
