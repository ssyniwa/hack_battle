import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="スート・コード：ネットワーク", page_icon="💻", layout="wide"
)


# ゲーム状態の初期化
def init_game():
  st.session_state.player_hp = 1000
  st.session_state.cpu_hp = 1000
  st.session_state.player_credits = 10
  st.session_state.cpu_credits = 10
  st.session_state.turn = 1
  st.session_state.game_over = False
  st.session_state.winner = None
  st.session_state.last_cpu_action = []  # 直前のCPUの行動ログ
  generate_deck_and_deal()


# デッキ生成と手札配布（プレイヤー・CPU共に8枚ずつに変更）
def generate_deck_and_deal():
  suits = ["♠", "♣", "♥", "♦"]
  suit_names = {
      "♠": "spade",
      "♣": "club",
      "♥": "heart",
      "♦": "diamond",
  }
  deck = []

  # 通常カードの生成 (4スート × 13数値 = 52枚)
  for suit in suits:
    for num in range(1, 14):
      img_filename = f"images/{suit_names[suit]}_{num}.jpg"
      deck.append({
          "type": "normal",
          "suit": suit,
          "val": num,
          "id": f"{suit}{num}",
          "img": img_filename,
      })

  # 特殊カード（バグ・AI）の追加
  deck.append({
      "type": "bug",
      "suit": "🌟",
      "val": 0,
      "id": "BUG-01",
      "img": "images/bug_card.jpg",
  })
  deck.append({
      "type": "ai",
      "suit": "🤖",
      "val": 10,
      "id": "AI-01",
      "img": "images/ai_card.jpg",
  })

  random.shuffle(deck)

  st.session_state.deck = deck
  st.session_state.discard_pile = []  # 捨て札置き場
  # プレイヤーとCPUにそれぞれ8枚ずつ手札を配る
  st.session_state.player_hand = [st.session_state.deck.pop() for _ in range(8)]
  st.session_state.cpu_hand = [st.session_state.deck.pop() for _ in range(8)]


# カード補充関数
def draw_card_for_player():
  if not st.session_state.deck:
    if st.session_state.discard_pile:
      st.session_state.deck = st.session_state.discard_pile
      st.session_state.discard_pile = []
      random.shuffle(st.session_state.deck)
      st.toast("🔄 山札が尽きたため、捨て札を再シャッフルしました！", icon="♻️")
    else:
      return None
  return st.session_state.deck.pop()


def draw_card_for_cpu():
  if not st.session_state.deck:
    if st.session_state.discard_pile:
      st.session_state.deck = st.session_state.discard_pile
      st.session_state.discard_pile = []
      random.shuffle(st.session_state.deck)
  if st.session_state.deck:
    return st.session_state.deck.pop()
  return None


if "player_hp" not in st.session_state:
  init_game()

# タイトル
st.title("💻 スート・コード：ネットワーク [拡張版]")
st.markdown(
    "**サイバーパンク・ハッキングバトル** — 8枚の手札から最大5枚を同時選択し、強力なコンボで敵を圧倒せよ！"
)

# ステータス表示
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(
      label="プレイヤー サーバー耐久 (HP)",
      value=f"{st.session_state.player_hp} / 1000",
  )
  st.metric(
      label="プレイヤー資金 (Credits)", value=f"{st.session_state.player_credits} ⚡"
  )
with col2:
  st.markdown(f"<h3 style='text-align: center;'>TURN {st.session_state.turn}</h3>", unsafe_allow_html=True)
  st.markdown(f"<p style='text-align: center; color: gray;'>山札残り: {len(st.session_state.deck)}枚 ｜ 捨て札: {len(st.session_state.discard_pile)}枚</p>", unsafe_allow_html=True)
with col3:
  st.metric(
      label="CPU サーバー耐久 (HP)", value=f"{st.session_state.cpu_hp} / 1000"
  )
  st.metric(label="CPU資金 (Credits)", value=f"{st.session_state.cpu_credits} ⚡")

st.divider()

# 直前のCPUの行動表示エリア
if "last_cpu_action" in st.session_state and st.session_state.last_cpu_action:
  st.markdown("### 🤖 直前のCPUのハッキング行動")
  cpu_cols = st.columns(len(st.session_state.last_cpu_action))
  for idx, c in enumerate(st.session_state.last_cpu_action):
    with cpu_cols[idx]:
      try:
        st.image(c["img"], width=120, caption=f"CPU: {c['id']}")
      except Exception:
        st.markdown(f"**{c['id']}**")
      st.text(f"属性:{c['suit']} / 値:{c['val']}")
  st.divider()

# 勝敗判定
if st.session_state.player_hp <= 0 or st.session_state.cpu_hp <= 0:
  st.session_state.game_over = True
  if st.session_state.player_hp <= 0 and st.session_state.cpu_hp <= 0:
    if st.session_state.player_credits >= st.session_state.cpu_credits:
      st.session_state.winner = "プレイヤー"
    else:
      st.session_state.winner = "CPU"
  elif st.session_state.player_hp <= 0:
    st.session_state.winner = "CPU"
  else:
    st.session_state.winner = "プレイヤー"

if st.session_state.game_over:
  if st.session_state.winner == "プレイヤー":
    st.balloons()
    st.success(f"🎉 ハッキング勝利！ 敵を制圧しました！（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")
  else:
    st.error(f"💥 ハッキング失敗… システムがロックアウトされました。（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")

  if st.button("🔄 システム再起動 (リトライ)"):
    init_game()
    st.rerun()
  st.stop()


# --- プレイヤーターン：複数カード選択（最大5枚） ---
st.subheader("🃏 サイバーデッキ（手札ターミナル・最大5枚選択可能）")
st.markdown("戦術に合わせて最大5枚のプロトコルを同時に選択し、強力なコンボを発動せよ。")

hand_options = {
    f"[{c['id']}] 属性: {c['suit']} ｜ 値: {c['val']} (インデックス:{i})": i
    for i, c in enumerate(st.session_state.player_hand)
}

selected_labels = st.multiselect(
    "同時に実行するカードを選択してください (最大5枚):",
    options=list(hand_options.keys()),
    max_selections=5  # 最大5枚に変更
)

selected_indices = [hand_options[label] for label in selected_labels]

if selected_indices:
  st.markdown("#### ⚡ 選択中のコマンドプレビュー")
  preview_cols = st.columns(len(selected_indices))
  for idx, card_i in enumerate(selected_indices):
    c = st.session_state.player_hand[card_i]
    with preview_cols[idx]:
      try:
        st.image(c["img"], width=150, caption=f"{c['id']}")
      except Exception:
        st.markdown(f"**{c['id']}**")
      st.text(f"属性:{c['suit']} / 値:{c['val']}")
else:
  st.info("💡 カードを1枚以上選択すると、コンボ効果や詳細を確認できます。")

st.divider()

# ターン実行ボタン
if st.button("🚀 選択したカードで一斉ハッキングを実行", type="primary", disabled=len(selected_indices) == 0):
  
  # --- プレイヤーのコンボ・効果処理 ---
  suits_played = [st.session_state.player_hand[i]['suit'] for i in selected_indices]
  vals_played = [st.session_state.player_hand[i]['val'] for i in selected_indices]
  
  suit_counts = {s: suits_played.count(s) for s in set(suits_played)}
  val_counts = {v: vals_played.count(v) for v in set(vals_played)}
  
  max_same_suit = max(suit_counts.values()) if suit_counts else 1
  suit_multiplier = 1.5 if max_same_suit >= 2 else 1.0
  if max_same_suit >= 3:
    suit_multiplier = 2.0

  has_number_pair = any(v >= 2 for v in val_counts.values())

  total_damage = 0
  total_heal = 0
  total_credits = 0

  sorted_indices = sorted(selected_indices, reverse=True)

  for card_i in sorted_indices:
    card = st.session_state.player_hand[card_i]
    
    if card["type"] == "normal":
      if card["suit"] == "♣":
        dmg = int(card["val"] * 2 * suit_multiplier)
        total_damage += dmg
      elif card["suit"] == "♠":
        hf = int(card["val"] * 2 * suit_multiplier)
        total_heal += hf
      elif card["suit"] == "♥":
        hf = int(card["val"] * 1.5 * suit_multiplier)
        total_heal += hf
      elif card["suit"] == "♦":
        cr = int(card["val"] * suit_multiplier)
        total_credits += cr

    elif card["type"] == "bug":
      effect_type = random.choice(["self_damage", "big_attack", "credit_boost"])
      if effect_type == "self_damage":
        st.session_state.player_hp -= 10
        st.toast("⚠️ バグ発生！ 10ダメージを受けた。", icon="💥")
      elif effect_type == "big_attack":
        total_damage += 30
      else:
        total_credits += 15

    elif card["type"] == "ai":
      total_damage += 25
      total_heal += 15
      total_credits += 10

    used_card = st.session_state.player_hand.pop(card_i)
    st.session_state.discard_pile.append(used_card)

  if has_number_pair:
    total_damage += 15
    total_credits += 10
    st.toast("✨【ペア・コンボ発動】同数字の共鳴により追加効果が発生！", icon="🔥")

  if max_same_suit >= 2:
    st.toast(f"🌊【スート・シナジー】同属性の同期により効果が {suit_multiplier}倍 に増幅！", icon="⚡")

  if total_damage > 0:
    st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - total_damage)
    st.toast(f"ウイルス攻撃成功！ CPUに {total_damage} のダメージ！", icon="🦠")
  if total_heal > 0:
    st.session_state.player_hp = min(1000, st.session_state.player_hp + total_heal)
    st.toast(f"システムが強化・修復され、HPが {total_heal} 回復！", icon="🛡️")
  if total_credits > 0:
    st.session_state.player_credits += total_credits
    st.toast(f"暗号通貨を大量調達！ +{total_credits} ⚡", icon="💠")

  # プレイヤーの補充
  cards_to_draw = len(selected_indices)
  for _ in range(cards_to_draw):
    new_c = draw_card_for_player()
    if new_c:
      st.session_state.player_hand.append(new_c)

  # --- CPUのターン処理（手札8枚からランダムに1〜5枚選んで一斉攻撃） ---
  st.session_state.last_cpu_action = []
  if st.session_state.cpu_hp > 0 and len(st.session_state.cpu_hand) > 0:
    # CPUが使う枚数をランダムに決定（1枚〜5枚、ただし手札の枚数以下）
    num_cpu_cards = random.randint(1, min(5, len(st.session_state.cpu_hand)))
    
    # 手札からランダムにインデックスを選択
    cpu_selected_indices = sorted(
        random.sample(range(len(st.session_state.cpu_hand)), num_cpu_cards),
        reverse=True
    )
    
    cpu_suits_played = []
    cpu_vals_played = []
    
    for idx in cpu_selected_indices:
      c = st.session_state.cpu_hand[idx]
      st.session_state.last_cpu_action.append(c)
      cpu_suits_played.append(c['suit'])
      cpu_vals_played.append(c['val'])

    # CPU側のコンボ計算
    cpu_suit_counts = {s: cpu_suits_played.count(s) for s in set(cpu_suits_played)}
    cpu_max_same_suit = max(cpu_suit_counts.values()) if cpu_suit_counts else 1
    cpu_suit_multiplier = 1.5 if cpu_max_same_suit >= 2 else 1.0
    if cpu_max_same_suit >= 3:
      cpu_suit_multiplier = 2.0

    cpu_total_dmg = 0
    cpu_total_heal = 0
    cpu_total_cr = 0

    for idx in cpu_selected_indices:
      c = st.session_state.cpu_hand.pop(idx)
      st.session_state.discard_pile.append(c)
      
      if c["type"] == "normal":
        if c["suit"] == "♣":
          cpu_total_dmg += int(c["val"] * 2 * cpu_suit_multiplier)
        elif c["suit"] == "♦":
          cpu_total_cr += int(c["val"] * cpu_suit_multiplier)
        else:
          cpu_total_heal += int(c["val"] * 1.5 * cpu_suit_multiplier)
      else:
        cpu_total_dmg += 20
        cpu_total_cr += 10

    if cpu_total_dmg > 0:
      st.session_state.player_hp = max(0, st.session_state.player_hp - cpu_total_dmg)
      st.toast(f"敵(CPU)のコンボ反撃！ {cpu_total_dmg} のダメージを受けた！", icon="🚨")
    if cpu_total_cr > 0:
      st.session_state.cpu_credits += cpu_total_cr
      st.toast(f"敵(CPU)が暗号資産を調達 (+{cpu_total_cr} ⚡)", icon="💰")
    if cpu_total_heal > 0:
      st.session_state.cpu_hp = min(1000, st.session_state.cpu_hp + cpu_total_heal)
      st.toast(f"敵(CPU)がシステムを修復しました。", icon="🔧")

    # CPUの手札補充
    for _ in range(num_cpu_cards):
      new_cpu_c = draw_card_for_cpu()
      if new_cpu_c:
        st.session_state.cpu_hand.append(new_cpu_c)

  st.session_state.turn += 1
  st.rerun()
