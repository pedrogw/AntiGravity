'use client';

import { useEffect, useState } from 'react';
import { AppError } from '@/domain/errors/AppError';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { usePlaces } from '@/hooks/usePlaces';
import { useUsers } from '@/hooks/useUsers';
import { useDeliveries } from '@/hooks/useDeliveries';

interface CriarEntregaDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CriarEntregaDialog({ open, onOpenChange }: CriarEntregaDialogProps) {
  const { factories, stores, listFactories, listStores } = usePlaces();
  const { drivers, fetchDrivers } = useUsers();
  const { createDelivery, isLoading } = useDeliveries();

  const [selectedFactory, setSelectedFactory] = useState('');
  const [selectedStore, setSelectedStore] = useState('');
  const [selectedDriver, setSelectedDriver] = useState('');
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    if (open) {
      listFactories();
      listStores();
      fetchDrivers();
    }
  }, [open, listFactories, listStores, fetchDrivers]);

  async function handleSubmit() {
    if (!selectedFactory || !selectedStore || !selectedDriver) return;

    setSubmitError('');
    try {
      await createDelivery(selectedFactory, selectedStore, selectedDriver);
      onOpenChange(false);
    } catch (err) {
      if (err instanceof AppError) {
        setSubmitError(err.message);
      } else {
        setSubmitError('Erro ao criar entrega.');
      }
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nova Entrega</DialogTitle>
          <DialogDescription>
            Preencha os campos abaixo para criar uma nova entrega.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="relative">
            <label className="text-sm font-medium mb-1 block">Fábrica</label>
            <Select value={selectedFactory} onValueChange={setSelectedFactory}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione uma fábrica" />
              </SelectTrigger>
              <SelectContent>
                {factories.map((f) => (
                  <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="relative">
            <label className="text-sm font-medium mb-1 block">Loja</label>
            <Select value={selectedStore} onValueChange={setSelectedStore}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione uma loja" />
              </SelectTrigger>
              <SelectContent>
                {stores.map((s) => (
                  <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="relative">
            <label className="text-sm font-medium mb-1 block">Motorista</label>
            <Select value={selectedDriver} onValueChange={setSelectedDriver}>
              <SelectTrigger>
                <SelectValue placeholder="Selecione um motorista" />
              </SelectTrigger>
              <SelectContent>
                {drivers.map((d) => (
                  <SelectItem key={d.id} value={d.id}>{d.email}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {submitError && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded" role="alert">
              {submitError}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancelar
          </Button>
          <Button onClick={handleSubmit} disabled={isLoading || !selectedFactory || !selectedStore || !selectedDriver}>
            {isLoading ? 'Criando...' : 'Criar'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
