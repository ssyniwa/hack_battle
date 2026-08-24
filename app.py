import itertools
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


# デッキ生成と手札配布（プレイヤー・CPU共に8枚ずつに変更）[cite: 3, 4]
def generate_deck_and_deal():
  suits = ["♠", "♣", "♥", "♦"]
  suit_names = {
      "♠": "spade",
      "♣": "club",
      "♥": "heart",
      "♦": "diamond",
  }
  deck = []

  # 通常カードの生成 (4スート × 13数値 = 52枚)[cite: 3, 4]
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

  # 特殊カード（バグ・AI）の追加[cite: 3, 4]
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
  st.session_state.discard_pile = []  # 捨て札置き場[cite: 3, 4]
  # プレイヤーとCPUにそれぞれ8枚ずつ手札を配る[cite: 3, 4]
  st.session_state.player_hand = [st.session_state.deck.pop() for _ in range(8)]
  st.session_state.cpu_hand = [st.session_state.deck.pop() for _ in range(8)]


# カード補充関数[cite: 3, 4]
def draw_card_for_player():
  if not st.session_state.deck:
    if st.session_state.discard_pile:
      st.session_state.deck = st.session_state.discard_pile
      st.session_state.discard_pile = []
      random.shuffle(st.session_state.deck)
      st.toast("🔄 山札が尽きたため、捨て札を再シャッフルしました！", icon="♻️")[cite: 3, 4]
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

# タイトル[cite: 3, 4]
st.title("💻 スート・コード：ネットワーク [拡張版]")
st.markdown(
    "**サイバーパンク・ハッキングバトル** — 8枚の手札から最大5枚を同時選択し、ポーカー役コンボで敵を圧倒せよ！"[cite: 3, 4]
)

# ステータス表示[cite: 3, 4]
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
  st.markdown(f"<h3 style='text-align: center;'>TURN {st.session_state.turn}</h3>", unsafe_allow_html=True)[cite: 3, 4]
  st.markdown(f"<p style='text-align: center; color: gray;'>山札残り: {len(st.session_state.deck)}枚 ｜ 捨て札: {len(st.session_state.discard_pile)}枚</p>", unsafe_allow_html=True)[cite: 3, 4]
with col3:
  st.metric(
      label="CPU サーバー耐久 (HP)", value=f"{st.session_state.cpu_hp} / 1000"
  )
  st.metric(label="CPU資金 (Credits)", value=f"{st.session_state.cpu_credits} ⚡")

st.divider()

# 直前のCPUの行動表示エリア[cite: 3, 4]
if "last_cpu_action" in st.session_state and st.session_state.last_cpu_action:
  st.markdown("### 🤖 直前のCPUのハッキング行動")[cite: 3, 4]
  cpu_cols = st.columns(len(st.session_state.last_cpu_action))
  for idx, c in enumerate(st.session_state.last_cpu_action):
    with cpu_cols[idx]:
      try:
        st.image(c["img"], width=200, caption=f"CPU: {c['id']}")[cite: 3, 4]
      except Exception:
        st.markdown(f"**{c['id']}**")[cite: 3, 4]
      st.text(f"属性:{c['suit']} / 値:{c['val']}")[cite: 3, 4]
  st.divider()

# 勝敗判定[cite: 3, 4]
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
    st.success(f"🎉 ハッキング勝利！ 敵を制圧しました！（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")[cite: 3, 4]
  else:
    st.error(f"💥 ハッキング失敗… システムがロックアウトされました。（最終資金: プレイヤー {st.session_state.player_credits} ⚡ vs CPU {st.session_state.cpu_credits} ⚡）")[cite: 3, 4]

  if st.button("🔄 システム再起動 (リトライ)"):
    init_game()
    st.rerun()
  st.stop()


# --- プレイヤーターン：複数カード選択（最大5枚） ---
st.subheader("🃏 サイバーデッキ（手札ターミナル・最大5枚選択可能）")[cite: 3, 4]
st.markdown("戦術に合わせて最大5枚のプロトコルを同時に選択し、強力なコンボを発動せよ。")[cite: 3, 4]

hand_options = {
    f"[{c['id']}] 属性: {c['suit']} ｜ 値: {c['val']} (インデックス:{i})": i
    for i, c in enumerate(st.session_state.player_hand)
}

selected_labels = st.multiselect(
    "同時に実行するカードを選択してください (最大5枚):",
    options=list(hand_options.keys()),
    max_selections=5,  # 最大5枚に変更[cite: 3, 4]
)

selected_indices = [hand_options[label] for label in selected_labels]

if selected_indices:
  st.markdown("#### ⚡ 選択中のコマンドプレビュー")[cite: 3, 4]
  preview_cols = st.columns(len(selected_indices))
  for idx, card_i in enumerate(selected_indices):
    c = st.session_state.player_hand[card_i]
    with preview_cols[idx]:
      try:
        st.image(c["img"], width=200, caption=f"{c['id']}")[cite: 3, 4]
      except Exception:
        st.markdown(f"**{c['id']}**")[cite: 3, 4]
      st.text(f"属性:{c['suit']} / 値:{c['val']}")[cite: 3, 4]
else:
  st.info("💡 カードを1枚以上選択すると、コンボ効果や詳細を確認できます。")[cite: 3, 4]

st.divider()


# 役判定用ヘルパー関数
def evaluate_poker_hands(cards):
  """選択されたカードリストからポーカー役を判定し、スコア(強さ)、役名、倍率、ボーナスを返す"""
  normal_cards = [c for c in cards if c["type"] == "normal"]
  if not normal_cards:
    return 0, "None", 1.0, 0, 0

  suits = [c["suit"] for c in normal_cards]
  vals = sorted([c["val"] for c in normal_cards])

  suit_counts = {s: suits.count(s) for s in set(suits)}
  val_counts = {v: vals.count(v) for v in set(vals)}

  max_same_val = max(val_counts.values()) if val_counts else 1
  max_same_suit = max(suit_counts.values()) if suit_counts else 1

  # ストレート判定
  is_straight = False
  if len(vals) >= 3 and len(set(vals)) == len(vals):
    if vals[-1] - vals[0] == len(vals) - 1:
      is_straight = True

  # フラッシュ判定
  is_flush = (max_same_suit >= len(normal_cards)) and (len(normal_cards) >= 3)

  # 役のランク付け（スコア化して最適選択に利用）
  if is_straight and is_flush:
    return 5, "ストレートフラッシュ", 3.0, 100, 50
  elif max_same_val >= 4:
    return 4, "フォーカード", 2.5, 80, 40
  elif max_same_val >= 3:
    return 3, "スリーカード", 2.0, 40, 20
  elif max_same_val >= 2:
    return 2, "ワンペア/ツーペア", 1.5, 15, 10
  else:
    return 1, "単発/なし", 1.0, 0, 0


# ターン実行ボタン
if st.button(
    "🚀 選択したカードで一斉ハッキングを実行",
    type="primary",
    disabled=len(selected_indices) == 0,
):

  # 選択されたカードオブジェクトのリスト
  chosen_cards = [st.session_state.player_hand[i] for i in selected_indices]

  # ポーカー役の評価
  _, hand_name, multiplier, bonus_dmg, bonus_cr = evaluate_poker_hands(
      chosen_cards
  )

  if hand_name != "単発/なし":
    st.toast(
        f"🌟【役成立: {hand_name}】効果が {multiplier}倍"
        " に増幅！追加ボーナス獲得！",
        icon="🔥",
    )

  total_damage = 0
  total_heal = 0
  total_credits = 0

  sorted_indices = sorted(selected_indices, reverse=True)

  for card_i in sorted_indices:
    card = st.session_state.player_hand[card_i]

    if card["type"] == "normal":
      if card["suit"] == "♣":
        dmg = int(card["val"] * 2 * multiplier)
        total_damage += dmg
      elif card["suit"] == "♠":
        hf = int(card["val"] * 2 * multiplier)
        total_heal += hf
      elif card["suit"] == "♥":
        hf = int(card["val"] * 1.5 * multiplier)
        total_heal += hf
      elif card["suit"] == "♦":
        cr = int(card["val"] * multiplier)
        total_credits += cr

    elif card["type"] == "bug":
      effect_type = random.choice(["self_damage", "big_attack", "credit_boost"])
      if effect_type == "self_damage":
        st.session_state.player_hp -= 10
        st.toast("⚠️ バグ発生！ 10ダメージを受けた。", icon="💥")
      elif effect_type == "big_attack":
        total_damage += int(30 * multiplier)
      else:
        total_credits += int(15 * multiplier)

    elif card["type"] == "ai":
      total_damage += int(25 * multiplier)
      total_heal += int(15 * multiplier)
      total_credits += int(10 * multiplier)

    used_card = st.session_state.player_hand.pop(card_i)
    st.session_state.discard_pile.append(used_card)

  # 役による固定ボーナスの加算
  total_damage += bonus_dmg
  total_credits += bonus_cr

  if total_damage > 0:
    st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - total_damage)
    st.toast(f"ウイルス攻撃成功！ CPUに {total_damage} のダメージ！", icon="🦠")
  if total_heal > 0:
    st.session_state.player_hp = min(
        1000, st.session_state.player_hp + total_heal
    )
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

  # --- CPUのターン処理（手札8枚から必ず最適な5枚を選んでコンボ実行） ---
  st.session_state.last_cpu_action = []
  if st.session_state.cpu_hp > 0 and len(st.session_state.cpu_hand) >= 5:
    best_combo_indices = None
    best_score = -1
    best_eval_result = None

    # 手札8枚から5枚を選ぶすべての組み合わせ（8C5 = 56通り）を検証し、最も強い役を選ぶ
    for combo in itertools.combinations(range(len(st.session_state.cpu_hand)), 5):
      combo_cards = [st.session_state.cpu_hand[i] for i in combo]
      score, h_name, mult, b_dmg, b_cr = evaluate_poker_hands(combo_cards)

      # 同点の場合は、合計数値やカード価値が高いものを優先するタイブレイカー
      tie_breaker = sum(
          c["val"] if c["type"] == "normal" else 10 for c in combo_cards
      )
      total_metric = score * 1000 + tie_breaker

      if total_metric > best_score:
        best_score = total_metric
        best_combo_indices = combo
        best_eval_result = (score, h_name, mult, b_dmg, b_cr)

    cpu_selected_indices = sorted(best_combo_indices, reverse=True)
    cpu_chosen_cards = [
        st.session_state.cpu_hand[idx] for idx in cpu_selected_indices
    ]

    for c in cpu_chosen_cards:
      st.session_state.last_cpu_action.append(c)

    _, cpu_hand_name, cpu_multiplier, cpu_bonus_dmg, _ = best_eval_result

    cpu_total_dmg = cpu_bonus_dmg
    cpu_total_heal = 0
    cpu_total_cr = 0

    for idx in cpu_selected_indices:
      c = st.session_state.cpu_hand.pop(idx)
      st.session_state.discard_pile.append(c)

      if c["type"] == "normal":
        if c["suit"] == "♣":
          cpu_total_dmg += int(c["val"] * 2 * cpu_multiplier)
        elif c["suit"] == "♦":
          cpu_total_cr += int(c["val"] * cpu_multiplier)
        else:
          cpu_total_heal += int(c["val"] * 1.5 * cpu_multiplier)
      else:
        cpu_total_dmg += int(20 * cpu_multiplier)
        cpu_total_cr += int(10 * cpu_multiplier)

    if cpu_total_dmg > 0:
      st.session_state.player_hp = max(
          0, st.session_state.player_hp - cpu_total_dmg
      )
      st.toast(
          f"敵(CPU)の最適コンボ反撃（役: {cpu_hand_name}）！ {cpu_total_dmg}"
          " のダメージ！",
          icon="🚨",
      )
    if cpu_total_cr > 0:
      st.session_state.cpu_credits += cpu_total_cr
      st.toast(f"敵(CPU)が暗号資産を調達 (+{cpu_total_cr} ⚡)", icon="💰")
    if cpu_total_heal > 0:
      st.session_state.cpu_hp = min(1000, st.session_state.cpu_hp + cpu_total_heal)
      st.toast(f"敵(CPU)がシステムを修復しました。", icon="🔧")

    # 消費した5枚分の手札を補充
    for _ in range(5):
      new_cpu_c = draw_card_for_cpu()
      if new_cpu_c:
        st.session_state.cpu_hand.append(new_cpu_c)

  st.session_state.turn += 1
  st.rerun()
