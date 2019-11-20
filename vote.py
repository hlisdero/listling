# Votes

# --- THINK BIG ---

class Items:
    class Votes:
        def vote(self) -> ItemChange: ...
        def unvote(self) -> ItemChange: ...

    def create(self) -> ItemsChange: ...

class ItemChange:
    position: Optional[Item]
    list_sum: float

class ItemsChange(ItemChange):
    item: Item

class ItemEvent(Event, ItemChange): ...

class ItemsEvent(Event, ItemsChange): ...

# - Maybe there is a better name than ItemChange or ItemResult?
# - Cool: Result of operation and Event mirrored / coupled tightly, Event wraps/encapsulates result
#   (here flat via inheritance, could also be via member, e.g. Event.detail: ItemChange)

# - Could also deliver events directly, no doppelgemoppel with result BUT API returning event is
#   really ugly (and getting Event after call without returning it also ugly)
# - We do not want to create json() on demand, ItemChange is value = immutable, but position sum etc
#   would change

# -> Können wir alles später entscheiden, und sogar am Anfang bei sort nur mit Event arbeiten

        #  def json(self, *, slc = None, include = False, user = UNDEFINED):
        #      return {
        #          **super().json(restricted=restricted, include=include, slc=slc),
        #          **({} if user is UNDEFINED else {'user_voted': self.has_user_voted(user)})
        #      }

class List:
    @property
    def items(self):
        indices = {
            'user': JSONRedisSequence(self.r, '{}.items'.format(self.id)),
            'time': ZSequence(self.r, '{}.items.by_time'.format(self.id)),
            'votes': ZSequence(self.r, '{}.items.by_votes'.format(self.id)),
            'tag': ZSequence(self.r, '{}.items.by_tag'.format(self.id))
        }
        return indices[self.sorted_by]

class Items:
    def _update(item):
        r.lrem(list_key, 1, item.id)
        r.zrem(votes_key, item.id)
        r.zrem(time_key, item.id)
        r.zrem(tag_key, '{}\0{}'.format(item.tags[0], item.id))
        r.zadd(votes_key, (len(item.votes), item.id))
        r.zadd(time_key, (item.time.time, item.id))
        r.zadd(tag_key, (0, '{}\0{}'.format(item.tags[0], item.id)))
