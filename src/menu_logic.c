#include "menu_logic.h"
#include <string.h>

static const int category_items[MENU_CATEGORIES][4] = {
  {0, 1, 2, -1}, {3, 4, 6, -1}, {5, 7, 8, 9}, {-1, -1, -1, -1}
};
static const int category_count[MENU_CATEGORIES] = {3,3,4,0};

void menu_init(MenuState *m) { memset(m, 0, sizeof(*m)); }

void menu_update(MenuState *m, uint32_t buttons) {
  uint32_t pressed = buttons & ~m->previous;
  int combo = (buttons & (BTN_L1|BTN_CIRCLE)) == (BTN_L1|BTN_CIRCLE);
  /* Un solo cambio por pulsación, incluso cuando el mando repite muestras. */
  if (combo && !m->combo_latched) {
    m->opened = !m->opened;
    m->combo_latched = 1;
    m->previous = buttons;
    return;
  }
  if (!combo) m->combo_latched = 0;
  if (!m->opened) { m->previous = buttons; return; }
  if (pressed & BTN_L2) {
    m->category = (m->category + MENU_CATEGORIES - 1) % MENU_CATEGORIES;
    m->selected = 0;
  } else if (pressed & BTN_R2) {
    m->category = (m->category + 1) % MENU_CATEGORIES;
    m->selected = 0;
  } else if (category_count[m->category] > 0) {
    if (pressed & BTN_UP) m->selected = (m->selected+category_count[m->category]-1)%category_count[m->category];
    else if (pressed & BTN_DOWN) m->selected = (m->selected+1)%category_count[m->category];
    else if (pressed & BTN_CROSS) {
      int id = category_items[m->category][m->selected];
      /* Los 9 trucos restantes dependen del maestro 0. */
      if (id == 0 || m->toggles[0]) {
        m->toggles[id] = !m->toggles[id];
        if (id == 0 && !m->toggles[0])
          for (int i=1; i<MENU_ITEMS; ++i) m->toggles[i]=0;
      }
    }
  }
  m->previous = buttons;
}
